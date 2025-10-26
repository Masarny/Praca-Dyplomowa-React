from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User
from datetime import timedelta
import traceback
import pyotp
import base64
import qrcode
from io import BytesIO

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Wymagana jest nazwa użytkownika i hasło."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Użytkownik już istnieje."}), 400

    try:
        hashed = generate_password_hash(password)
        secret = pyotp.random_base32()
        user = User(username=username, password_hash=hashed, totp_secret=secret)
        db.session.add(user)
        db.session.commit()

        # Tworzymy URI dla aplikacji Google Authenticator
        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="TwojaAplikacja")

        # Generujemy obrazek QR z URI
        qr = qrcode.make(otp_uri)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        return jsonify({
            "message": "Użytkownik zarejestrował się pomyślnie.",
            "username": user.username,
            "otp_uri": otp_uri,
            "qr_code": f"data:image/png;base64,{qr_base64}"
        }), 201
    except Exception:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({"error": "Błąd rejestracji użytkownika."}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Wymagana jest nazwa użytkownika i hasło."}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Nieprawidłowa nazwa użytkownika lub hasło."}), 401

    try:
        return jsonify({"message": "Dane poprawne – wymagany TOTP."}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd podczas weryfikacji danych logowania."}), 500


@auth_bp.route("/verify_totp", methods=["POST"])
def verify_totp_login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    totp_code = data.get("totp") or ""

    if not username or not totp_code:
        return jsonify({"error": "Brak danych do weryfikacji."}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.totp_secret:
        return jsonify({"error": "Nie znaleziono użytkownika lub brak skonfigurowanego TOTP."}), 404

    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(totp_code, valid_window=1):
        return jsonify({"error": "Nieprawidłowy kod TOTP."}), 401

    try:
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token, "username": user.username}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd generowania tokenu JWT."}), 500


@auth_bp.route("/verify_totp_auth", methods=["POST"])
@jwt_required()
def verify_totp_auth():
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        totp_code = data.get("totp") or ""
        if not totp_code:
            return jsonify({"error": "Brak kodu TOTP."}), 400

        user = User.query.get(user_id)
        if not user or not user.totp_secret:
            return jsonify({"error": "Nie znaleziono użytkownika lub TOTP nie jest skonfigurowany."}), 404

        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(totp_code, valid_window=1):
            return jsonify({"message": "Kod TOTP jest prawidłowy."}), 200
        else:
            return jsonify({"error": "Nieprawidłowy kod TOTP."}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd podczas weryfikacji TOTP."}), 500


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Użytkownik nie istnieje."}), 404
        return jsonify({"username": user.username}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd pobierania danych użytkownika."}), 500
