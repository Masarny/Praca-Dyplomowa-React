from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User
from datetime import timedelta
import traceback


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
        user = User(username=username, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Użytkownik zarejestrował się pomyślnie.", "username": user.username}), 201
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
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token, "username": user.username}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd generowania tokenu JWT."}), 500


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