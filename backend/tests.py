from flask import Blueprint, jsonify, request
from translation import polish, translate_crack_time_string
from zxcvbn import zxcvbn
import re, math, random


tests_bp = Blueprint("tests_bp", __name__)


@tests_bp.route("/test_password", methods=["POST"])
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


@tests_bp.route("/improve_password", methods=["POST"])
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
