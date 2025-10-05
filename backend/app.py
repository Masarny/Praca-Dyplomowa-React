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
        word_count = int(request.args.get("count", 6))
    except ValueError:
        return jsonify({"error": "Invalid count"}), 400

    if word_count < 1 or word_count > 32:
        return jsonify({"error": "Count must be between 1 and 32"}), 400

    DICEWARE_WORDS = {}

    try:
        with open("dicts/dice-directory.txt", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    key, word = parts
                    DICEWARE_WORDS[key] = word
    except FileNotFoundError:
        return jsonify({"error": "Missing diceware dictionary file"}), 500
    
    words = []

    for _ in range(word_count):
        while True:
            key = "".join(str(random.randint(1, 6)) for _ in range(5))
            if key in DICEWARE_WORDS:
                words.append(DICEWARE_WORDS[key])
                break

    password = " ".join(words)

    return jsonify({"password": password})


@app.route("/api/generate_passphrase")
def generate_passphrase():
    try:
        count = int(request.args.get("count", 4))
    except ValueError:
        return jsonify({"error": "Invalid count"}), 400

    if count < 1 or count > 32:
        return jsonify({"error": "Count must be between 1 and 32"}), 400

    words = []

    try:
        with open("dicts/dice-directory.txt", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    _, word = parts
                    words.append(word)
    except FileNotFoundError:
        return jsonify({"error": "Missing diceware dictionary file"}), 500

    separators = ["-", "_", ".", "~"]
    sep = secrets.choice(separators)
    phrase = sep.join(secrets.choice(words).capitalize() for _ in range(count))
    if secrets.randbelow(2):
        phrase += str(secrets.randbelow(100))
    return jsonify({"password": phrase})


@app.route("/api/test_password", methods=["POST"])
def test_password():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    try:
        with open("dicts/commonWords.json", encoding="utf-8") as pol_dict:
            polish_dict = json.load(pol_dict)
        add_frequency_lists({'common_words': polish_dict})
    except Exception:
        polish_dict = []

    data = zxcvbn(password)
    feedback = data["feedback"]
    crack_time = data["crack_times_display"]["offline_slow_hashing_1e4_per_second"]
    polish_crack_time = translate_crack_time_string(crack_time)
    
    if isinstance(feedback["warning"], list):
        warnings = [polish["warning"].get(w, w) for w in feedback["warning"]]
    elif feedback["warning"]:
        warnings = [polish["warning"].get(feedback["warning"], feedback["warning"])]
    else:
        warnings = ["Brak ostrzeżeń!"]

    if isinstance(feedback["suggestions"], list):
        suggestions = [polish["suggestions"].get(s, s) for s in feedback["suggestions"]]
    elif feedback["suggestions"]:
        suggestions = [polish["suggestions"].get(feedback["suggestions"], feedback["suggestions"])]
    else:
        suggestions = ["Brak sugestii!"]

    return jsonify({
        "strength": data["score"],  # liczba 0–4
        "warnings": warnings,
        "suggestions": suggestions,
        "crack_time": polish_crack_time
    })

    
if __name__ == "__main__":
    app.run(debug=True)

