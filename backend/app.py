from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import secrets
import string
import random
import json
import re
from zxcvbn import zxcvbn
from zxcvbn.matching import add_frequency_lists
from translation import polish, translate_crack_time_string  # zakładam, że masz te pliki w katalogu app/


app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)


@app.route("/")
def serve_react_app():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/generate")
def generate_password():
    try:
        length = int(request.args.get("length", 24))
    except ValueError:
        return jsonify({"error": "Invalid length"}), 400

    if length < 8 or length > 128:
        return jsonify({"error": "Length must be between 8 and 128"}), 400

    alphabet = string.ascii_letters + string.digits + string.punctuation

    password = "".join(secrets.choice(alphabet) for _ in range(length))

    return jsonify({"password": password})


@app.route("/api/generate_diceware")
def generate_diceware():
    try:
        count = int(request.args.get("count", 5))
    except ValueError:
        return jsonify({"error": "Invalid count"}), 400

    if count < 1 or count > 32:
        return jsonify({"error": "Count must be between 1 and 32"}), 400

    sep_param = request.args.get("sep", "space").lower()
    sep_map = {
        "space": " ",
        "dash": "-",
        "underscore": "_",
        "slash": "/",
    }

    if sep_param == "random":
        separator = random.choice(list(sep_map.values()))
    else:
        separator = sep_map.get(sep_param)

    if separator is None:
        return jsonify({"error": "Invalid separator"}), 400

    DICEWARE_WORDS = {}

    try:
        with open("dicts/dice-directory.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    key, word = parts[0], parts[1]
                    DICEWARE_WORDS[key] = word
    except FileNotFoundError:
        return jsonify({"error": "Diceware dictionary file not found"}), 500
    
    words = []

    for _ in range(count):
        while True:
            key = "".join(str(random.randint(1, 6)) for _ in range(5))
            if key in DICEWARE_WORDS:
                words.append(DICEWARE_WORDS[key])
                break

    password = separator.join(words)

    return jsonify({
        "password": password,
        "separator_used": separator  # frontend może to wyświetlić, jeśli chcesz
    })


@app.route("/api/test_password", methods=["POST"])
def test_password():
    import math
    from zxcvbn import zxcvbn
    import json

    data = request.json or {}
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    try:
        from translation import polish as polish_translations, translate_crack_time_string
    except Exception:
        polish_translations = {
            "warning": {
                "straight_rows_of_keys": "Unikaj prostych sekwencji klawiszy jak 'qwerty'.",
                "key_pattern": "Unikaj wzorców na klawiaturze.",
                "simple_repeat": "Hasło zawiera powtarzające się znaki.",
                "repeated_pattern": "Hasło składa się z powtórzeń wzorca.",
                "digits_only": "Hasło składa się tylko z cyfr.",
                "common_words": "Hasło zawiera powszechne słowa."
            },
            "suggestions": {
                "use_a_longer_password": "Użyj dłuższego hasła.",
                "add_another_word": "Dodaj kolejne słowo.",
                "capitalize_different_letters": "Zmieniaj wielkość liter w losowych miejscach.",
                "add_numbers_or_symbols": "Dodaj cyfry lub symbole.",
                "avoid_common_words": "Unikaj powszechnych słów i fraz."
            }
        }

        def translate_crack_time_string(s):
            if not isinstance(s, str):
                return s
            mapping = {
                "less than a second": "mniej niż sekunda",
                "seconds": "sekundy",
                "minutes": "minuty",
                "hours": "godziny",
                "days": "dni",
                "months": "miesiące",
                "centuries": "stulecia",
                "Unknown": "Nieznany"
            }
            for en, pl in mapping.items():
                if en in s:
                    return s.replace(en, pl)
            return s

    words = re.findall(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", password)
    word_count = len(words)

    try:
        result = zxcvbn(password)
        z_score = int(result.get("score", 0))  # 0..4
        z_feedback = result.get("feedback", {}) or {}
        z_crack_time = result.get("crack_times_display", {}).get("offline_slow_hashing_1e4_per_second", "Unknown")
    except Exception:
        z_score = 0
        z_feedback = {}
        z_crack_time = "Unknown"

    if word_count >= 3:
        entropy = math.log2((7776) ** word_count)
        if entropy < 40:
            score = 1
        elif entropy < 60:
            score = 2
        elif entropy < 80:
            score = 3
        else:
            score = 4
        crack_time = f"{round(entropy, 1)} bity entropii"
    else:
        score = z_score
        crack_time = translate_crack_time_string(z_crack_time)

    warnings = []
    suggestions = []

    z_warn = z_feedback.get("warning")
    z_sugs = z_feedback.get("suggestions", [])

    def translate_warning(w):
        if not w:
            return None
        if isinstance(w, str):
            for key, val in polish_translations.get("warning", {}).items():
                if key.replace('_', ' ') in w.lower() or key in w:
                    return val
            return w

    def translate_suggestion(s):
        if not s:
            return None
        for key, val in polish_translations.get("suggestions", {}).items():
            if key.replace('_', ' ') in s.lower() or key in s:
                return val
        return s

    if isinstance(z_warn, list):
        for w in z_warn:
            tw = translate_warning(w)
            if tw:
                warnings.append(tw)
    elif isinstance(z_warn, str) and z_warn:
        tw = translate_warning(z_warn)
        if tw:
            warnings.append(tw)

    if isinstance(z_sugs, list):
        for s in z_sugs:
            ts = translate_suggestion(s)
            if ts:
                suggestions.append(ts)

    if len(password) < 8:
        suggestions.append("Użyj co najmniej 8 znaków.")
    if not re.search(r"[A-ZĄĆĘŁŃÓŚŹŻ]", password):
        suggestions.append("Dodaj wielkie litery.")
    if not re.search(r"\d", password):
        suggestions.append("Dodaj co najmniej jedną cyfrę.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append("Dodaj znaki specjalne (np. @, #, $).")
    if word_count >= 3:
        suggestions.append("Passphrase z kilkoma losowymi słowami to dobry wybór — nie zmieniaj ich kolejności.")
    if word_count > 12:
        warnings.append("Bardzo długie passphrase może być trudne do zapamiętania.")

    def uniq_preserve(seq):
        seen = set()
        out = []
        for item in seq:
            if item not in seen:
                seen.add(item)
                out.append(item)
        return out

    warnings = uniq_preserve(warnings) or ["Brak ostrzeżeń!"]
    suggestions = uniq_preserve(suggestions) or ["Brak sugestii!"]

    labels = ["Bardzo słabe", "Słabe", "Średnie", "Silne", "Bardzo silne"]
    score = max(0, min(4, int(score)))
    strength_label = labels[score]

    return jsonify({
        "strength": strength_label,
        "score": score,
        "warnings": warnings,
        "suggestions": suggestions,
        "crack_time": crack_time
    })


@app.route("/api/guidelines")
def get_guidelines():
    guidelines = {
        "Hasła": [
            "Placeholder.",
            "Placeholder.",
            "Placeholder.",
            "Placeholder.",
            "Placeholder."
        ],
        "Uwierzytelnianie": [
            "Placeholder.",
            "Placeholder.",
            "Placeholder.",
            "Placeholder."
        ],
        "Cyberbezpieczeństwo": [
            "Placeholder.",
            "Placeholder.",
            "Placeholder.",
            "Placeholder.",
            "Placeholder."
        ]
    }
    return jsonify(guidelines)

  
if __name__ == "__main__":
    app.run(debug=True)

