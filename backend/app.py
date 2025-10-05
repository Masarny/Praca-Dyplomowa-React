from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import secrets
import string
import re


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


@app.route("/api/test_password", methods=["POST"])
def test_password():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    # --- ANALIZA HASEŁ ---
    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    strength_points = sum([has_lower, has_upper, has_digit, has_symbol])
    score = strength_points + (1 if length >= 12 else 0) + (1 if length >= 20 else 0)

    if score <= 2:
        strength = "Weak"
        crack_time = "less than a second"
    elif score == 3:
        strength = "Medium"
        crack_time = "a few minutes"
    elif score == 4:
        strength = "Strong"
        crack_time = "hours"
    else:
        strength = "Very Strong"
        crack_time = "days or more"

    warnings = []
    suggestions = []

    if length < 8:
        warnings.append("Password is too short.")
        suggestions.append("Use at least 8 characters.")
    if not has_upper:
        suggestions.append("Add uppercase letters.")
    if not has_digit:
        suggestions.append("Include at least one digit.")
    if not has_symbol:
        suggestions.append("Add special symbols (e.g. @, #, $, !).")

    return jsonify({
        "strength": strength,
        "warnings": warnings,
        "suggestions": suggestions,
        "crack_time": crack_time
    })


if __name__ == "__main__":
    app.run(debug=True)

