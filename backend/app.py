from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from database import db
from auth import auth_bp
from passwords import passwords_bp
from translation import polish, translate_crack_time_string
from zxcvbn import zxcvbn
import string, secrets, random, re, math, os, traceback
from datetime import timedelta
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv


app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")


CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super_secret_jwt_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

db.init_app(app)
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(passwords_bp, url_prefix="/api/passwords")


load_dotenv()


with app.app_context():
    db.create_all()


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Brak nagłówka Authorization lub nieprawidłowy token."}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Nieprawidłowy token JWT."}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token JWT wygasł. Zaloguj się ponownie."}), 401


@app.route("/")
def serve_index():
    try:
        return send_from_directory(app.static_folder, "index.html")
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "frontend not found", "error": str(e)}), 200


@app.route("/api/generate")
def generate_password():
    try:
        length = int(request.args.get("length", 24))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid length"}), 400
    if length < 4 or length > 256:
        return jsonify({"error": "Length range 4..256"}), 400

    alphabet = string.ascii_letters + string.digits + string.punctuation
    return jsonify({"password": "".join(secrets.choice(alphabet) for _ in range(length))})


@app.route("/api/generate_diceware")
def generate_diceware():
    try:
        count = int(request.args.get("count", 5))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid count"}), 400
    if count < 1 or count > 32:
        return jsonify({"error": "Count between 1 and 32"}), 400

    sep_param = (request.args.get("sep") or "space").lower()
    sep_map = {"space":" ", "dash":"-", "underscore":"_", "slash":"/"}

    if sep_param == "random":
        separator = None  # specjalny przypadek — losowy dla każdego odstępu
    else:
        separator = sep_map.get(sep_param)

    if sep_param != "random" and separator is None:
        return jsonify({"error": "Invalid separator"}), 400

    dice_path = os.path.join("dicts", "dice-directory.txt")

    D = {}

    try:
        with open(dice_path, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    D[parts[0]] = parts[1]
    except FileNotFoundError:
        return jsonify({"error":"Missing dice list file"}), 500

    words = []

    for _ in range(count):
        while True:
            key = "".join(str(random.randint(1,6)) for _ in range(5))
            if key in D:
                words.append(D[key]); break

    if sep_param == "random":
        sep_values = list(sep_map.values())
        password = "".join(
            word + (random.choice(sep_values) if i < len(words) - 1 else "")
            for i, word in enumerate(words)
        )
    else:
        password = separator.join(words)

    return jsonify({"password": password})


@app.route("/api/generate_from_phrase", methods=["POST"])
def generate_from_phrase():
    data = request.get_json() or {}
    phrase = data.get("phrase", "").strip()
    if not phrase:
        return jsonify({"error": "Brak zdania wejściowego."}), 400

    phrase = re.sub(r"\s+", " ", phrase)

    specials = ["@", "#", "$", "%", "&", "!", "*", "_", "-", "="]
    separator = random.choice(["_", "-", "@"])

    words = phrase.split(" ")
    password = separator.join(words)

    def smart_case(word):
        result = ""
        for ch in word:
            if ch.isalpha():
                if random.random() < 0.25:
                    result += ch.upper()
                else:
                    result += ch.lower()
            else:
                result += ch
        return result

    password = separator.join(smart_case(w) for w in words)

    prefix = random.choice(specials) if random.random() < 0.7 else ""
    suffix = ""

    if random.random() < 0.9:
        suffix += str(random.randint(10, 9999))
    if random.random() < 0.8:
        suffix += random.choice(specials)

    strong_password = f"{prefix}{password}{suffix}"

    if not any(c.isdigit() for c in strong_password):
        strong_password += str(random.randint(1, 99))
    if not re.search(r"[!@#$%^&*()_+=\-]", strong_password):
        strong_password += random.choice(specials)
    if not any(c.isupper() for c in strong_password):
        chars = list(strong_password)
        for i in range(0, len(chars), max(1, len(chars)//6)):
            if chars[i].isalpha():
                chars[i] = chars[i].upper()
        strong_password = "".join(chars)

    return jsonify({"password": strong_password})


@app.route("/api/test_password", methods=["POST"])
def test_password():
    data = request.get_json() or {}
    password = data.get("password", "")
    if not password:
        return jsonify({"error":"Password required"}), 400

    try:
        res = zxcvbn(password)
        z_score = int(res.get("score",0))
        z_feedback = res.get("feedback",{}) or {}
        z_crack = res.get("crack_times_display",{}).get("offline_slow_hashing_1e4_per_second","Unknown")
    except Exception:
        z_score = 0; z_feedback = {}; z_crack = "Unknown"

    words = re.findall(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", password)
    word_count = len(words)

    if word_count >= 3:
        entropy = math.log2(7776 ** word_count)
        if entropy < 40: score = 1
        elif entropy < 60: score = 2
        elif entropy < 80: score = 3
        else: score = 4
        crack_time = f"{round(entropy,1)} bity entropii"
    else:
        score = z_score
        try:
            crack_time = translate_crack_time_string(z_crack)
        except Exception:
            crack_time = z_crack

    warnings = []
    suggestions = []
    z_warn = z_feedback.get("warning")
    z_sugs = z_feedback.get("suggestions", [])

    try:
        trans = __import__('translation').polish
    except Exception:
        trans = {"warning":{}, "suggestions":{}}

    def translate_msg(m, map_dict):
        if not m: return None
        if m in map_dict: return map_dict[m]
        low = m.lower()
        for k,v in map_dict.items():
            if k.lower() in low: return v
        return m

    for w in (z_warn if isinstance(z_warn,list) else ([z_warn] if z_warn else [])):
        t = translate_msg(w, trans.get("warning", {})); 
        if t: warnings.append(t)

    for s in z_sugs:
        t = translate_msg(s, trans.get("suggestions", {})); 
        if t: suggestions.append(t)

    common_patterns = ["password", "qwerty", "12345", "admin", "letmein", "welcome", "abc123"]
    for pat in common_patterns:
        if pat.lower() in password.lower():
            warnings.append(f"Hasło zawiera popularny wzorzec: '{pat}'.")

    if len(set(password)) < len(password) / 2:
        warnings.append("Zbyt wiele powtarzających się znaków — zwiększ różnorodność.")

    charset_size = 0
    if re.search(r"[a-z]", password): charset_size += 26
    if re.search(r"[A-Z]", password): charset_size += 26
    if re.search(r"\d", password): charset_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset_size += 20
    if charset_size > 0:
        estimated_entropy = math.log2(charset_size ** len(password))
        suggestions.append(f"Szacowana entropia: ok. {round(estimated_entropy,1)} bitów.")

    keyboard_patterns = ["qwerty", "asdf", "zxcv", "1234", "0987"]
    for seq in keyboard_patterns:
        if seq in password.lower():
            warnings.append(f"Unikaj sekwencji klawiaturowych jak '{seq}'.")

    weak_words = ["haslo", "tajne", "moje", "user", "login", "kot", "pies"]
    for w in weak_words:
        if re.search(rf"\b{w}\b", password.lower()):
            warnings.append(f"Hasło zawiera łatwe do odgadnięcia słowo: '{w}'.")

    if len(password) < 8: suggestions.append("Użyj co najmniej 8 znaków.")
    if not re.search(r"[A-ZĄĆĘŁŃÓŚŹŻ]", password): suggestions.append("Dodaj wielkie litery.")
    if not re.search(r"\d", password): suggestions.append("Dodaj co najmniej jedną cyfrę.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): suggestions.append("Dodaj znaki specjalne (np. @, #, $).")
    if word_count >= 3: suggestions.append("Passphrase z kilkoma losowymi słowami to dobry wybór — nie zmieniaj ich kolejności.")
    if word_count > 12: warnings.append("Bardzo długie passphrase może być trudne do zapamiętania.")

    def uniq(seq):
        seen=set(); out=[]
        for x in seq:
            if x not in seen:
                seen.add(x); out.append(x)
        return out

    warnings = uniq(warnings) or ["Brak ostrzeżeń!"]
    suggestions = uniq(suggestions) or ["Brak sugestii!"]
    labels = ["Bardzo słabe","Słabe","Średnie","Silne","Bardzo silne"]
    score = max(0,min(4,int(score)))

    return jsonify({
        "strength": labels[score],
        "score": score,
        "warnings": warnings,
        "suggestions": suggestions,
        "crack_time": crack_time
    })


@app.route("/api/guidelines")
def get_guidelines():
    return jsonify({
        "Cyberbezpieczeństwo": [
            "Placeholder cyberbezpieczeństwo 1.",
            "Placeholder cyberbezpieczeństwo 2.",
            "Placeholder cyberbezpieczeństwo 3."
        ],
        "Bezpieczne Hasła": [
            "Placeholder bezpieczne hasła 1.",
            "Placeholder bezpieczne hasła 2.",
            "Placeholder bezpieczne hasła 3."
        ],
        "Uwierzytelnianie": [
            "Placeholder uwierzytelnianie 1.",
            "Placeholder uwierzytelnianie 2.",
            "Placeholder uwierzytelnianie 3."
        ],
        "Ataki na Użytkowników": [
            "Placeholder ataki 1.",
            "Placeholder ataki 2.",
            "Placeholder ataki 3."
        ]
    })


@app.route("/api/improve_password", methods=["POST"])
def improve_password():
    data = request.get_json() or {}
    password = data.get("password", "").strip()
    if not password:
        return jsonify({"error": "Brak hasła do ulepszenia."}), 400

    specials = ["@", "#", "$", "%", "&", "!", "*", "_", "-", "+", "?"]
    digits = "0123456789"

    words = re.split(r"\s+", password)

    def stylize_word(word):
        if not word:
            return ""
        result = ""
        for i, ch in enumerate(word):
            if ch.isalpha():
                if i == 0 or random.random() < 0.3:
                    result += ch.upper()
                else:
                    result += ch.lower()
            else:
                result += ch
        return result

    styled_words = [stylize_word(w) for w in words]

    separator = random.choice(["_", "-", "@", ""])

    improved_core = separator.join(styled_words)

    prefix = ""
    suffix = ""

    if random.random() < 0.7:
        prefix = random.choice(specials)

    suffix = str(random.randint(1000, 9999)) + random.choice(specials)

    improved_password = f"{prefix}{improved_core}{suffix}"

    if not any(c.isdigit() for c in improved_password):
        improved_password += str(random.randint(1, 99))
    if not re.search(r"[!@#$%^&*()_+\-?]", improved_password):
        improved_password += random.choice(specials)
    if not any(c.isupper() for c in improved_password):
        improved_password = improved_password[0].upper() + improved_password[1:]

    improved_password = re.sub(r"\s+", "_", improved_password)

    return jsonify({"improved_password": improved_password})


if __name__ == "__main__":
    app.run(debug=True)
