from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from database import db
from auth import auth_bp
from passwords import passwords_bp
from generation import generation_bp
from tests import tests_bp
from guidelines import guidelines_bp
from translation import polish, translate_crack_time_string
from zxcvbn import zxcvbn
import string, secrets, random, re, math, os, traceback
from datetime import timedelta
from flask_jwt_extended import JWTManager


from dotenv import load_dotenv
load_dotenv()
if not os.environ.get("JWT_SECRET_KEY"):
    print("Uwaga: Brak JWT_SECRET_KEY w .env – używany klucz domyślny!")
if not os.environ.get("FERNET_KEY"):
    print("Uwaga: Brak FERNET_KEY w .env – szyfrowanie haseł nie będzie bezpieczne!")

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
app.register_blueprint(generation_bp, url_prefix="/api")
app.register_blueprint(tests_bp, url_prefix="/api")
app.register_blueprint(guidelines_bp, url_prefix="/api")


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


@app.errorhandler(Exception)
def handle_exception(e):
    """Globalna obsługa wyjątków"""
    print("=== Błąd backendu ===")
    traceback.print_exc()

    # Jeśli to błąd HTTP, zwróć jego kod
    from werkzeug.exceptions import HTTPException
    if isinstance(e, HTTPException):
        return jsonify({
            "error": e.description,
            "status": e.code
        }), e.code

    # Inne błędy — 500 Internal Server Error
    return jsonify({
        "error": "Wewnętrzny błąd serwera",
        "details": str(e)
    }), 500


if __name__ == "__main__":
    app.run(debug=True)
