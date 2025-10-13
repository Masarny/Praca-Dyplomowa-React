from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from database import db
from auth import auth_bp
from passwords import passwords_bp
from translation import polish, translate_crack_time_string
from zxcvbn import zxcvbn
import string, secrets, random, re, math
import os


app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")


CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev_jwt_secret_change_me")


db.init_app(app)


from flask_jwt_extended import JWTManager
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(passwords_bp, url_prefix="/api/passwords")


with app.app_context():
    db.create_all()


@app.route("/")
def serve_index():
    try:
        return send_from_directory(app.static_folder, "index.html")
    except Exception:
        return jsonify({"status": "ok"}), 200


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
        separator = random.choice(list(sep_map.values()))
    else:
        separator = sep_map.get(sep_param)
    if separator is None:
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

    return jsonify({"password": separator.join(words)})


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
    return jsonify({"strength": labels[score], "score": score, "warnings": warnings, "suggestions": suggestions, "crack_time": crack_time})


@app.route("/api/guidelines")
def get_guidelines():
    return jsonify({
        "Hasła": [
            "Placeholder.",
            "Placeholder.",
            "Placeholder."
        ],
        "Uwierzytelnianie": [
            "Placeholder.",
            "Placeholder."
        ],
        "Cyberbezpieczeństwo": [
            "Placeholder.",
            "Placeholder."
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)
