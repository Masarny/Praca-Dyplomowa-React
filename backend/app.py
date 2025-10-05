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
    """
    Checks password strength using zxcvbn + entropy logic for passphrases.
    Returns detailed feedback, suggestions, and estimated crack time.
    """
    import math
    from zxcvbn import zxcvbn

    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    words = re.findall(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", password)
    word_count = len(words)

    try:
        result = zxcvbn(password)
        strength_score = result["score"]
        feedback = result.get("feedback", {})
        crack_time = result["crack_times_display"]["offline_slow_hashing_1e4_per_second"]
    except Exception:
        strength_score = 0
        feedback = {}
        crack_time = "Unknown"

    if word_count >= 3:
        entropy = math.log2(7776 ** word_count)  # Diceware word list entropy
        if entropy < 40:
            strength_score = 1
        elif entropy < 60:
            strength_score = 2
        elif entropy < 80:
            strength_score = 3
        else:
            strength_score = 4
        crack_time = f"{round(entropy, 1)} bits of entropy"

    warnings = []
    suggestions = []

    if feedback.get("warning"):
        warnings.append(feedback["warning"])

    for s in feedback.get("suggestions", []):
        suggestions.append(s)

    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if not re.search(r"[A-ZĄĆĘŁŃÓŚŹŻ]", password):
        suggestions.append("Add uppercase letters.")
    if not re.search(r"\d", password):
        suggestions.append("Include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append("Add special characters (e.g. @, #, $, !).")
    if word_count >= 3:
        suggestions.append("Passphrases with multiple random words are a great choice.")
    if word_count > 8:
        warnings.append("Overly long passphrases may be hard to remember.")

    labels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    strength_label = labels[strength_score]

    return jsonify({
        "strength": strength_label,
        "score": strength_score,
        "warnings": warnings or ["No warnings!"],
        "suggestions": suggestions or ["No suggestions!"],
        "crack_time": crack_time
    })


@app.route("/api/guidelines")
def get_guidelines():
    guidelines = {
        "Passwords": [
            "Use at least 12–16 characters.",
            "Mix uppercase, lowercase, numbers, and symbols.",
            "Avoid dictionary words or personal info.",
            "Use a passphrase made of random words for stronger security.",
            "Never reuse passwords between sites."
        ],
        "Authentication": [
            "Enable two-factor authentication (2FA) whenever possible.",
            "Use an authenticator app instead of SMS codes.",
            "Don’t share authentication codes or backup keys.",
            "Review active sessions and revoke unknown devices."
        ],
        "Cybersecurity": [
            "Keep your system and browser up to date.",
            "Be careful with links and attachments in emails.",
            "Use a VPN on public Wi-Fi networks.",
            "Regularly back up your important data.",
            "Lock your device when you step away."
        ]
    }
    return jsonify(guidelines)

  
if __name__ == "__main__":
    app.run(debug=True)

