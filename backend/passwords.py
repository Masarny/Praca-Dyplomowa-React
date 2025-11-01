from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import StoredPassword, User
from encryption_utils import encrypt_text, decrypt_text
import re, traceback


passwords_bp = Blueprint("passwords_bp", __name__)


def safe_encrypt(value: str) -> str:
    if not value:
        return ""
    try:
        return encrypt_text(value)
    except Exception as e:
        print("Błąd szyfrowania:", e)
        return value


def safe_decrypt(value: str) -> str:
    if not value:
        return ""
    try:
        return decrypt_text(value)
    except Exception as e:
        print("Błąd deszyfrowania:", e)
        return value


@passwords_bp.route("/", methods=["GET"])
@jwt_required()
def get_passwords():
    try:
        user_id = get_jwt_identity()
        passwords = StoredPassword.query.filter_by(user_id=user_id).all()

        result = []
        for p in passwords:
            result.append({
                "id": p.id,
                "site": safe_decrypt(p.site),
                "login": safe_decrypt(p.login),
                "password": safe_decrypt(p.password),
                "notes": safe_decrypt(p.notes)
            })

        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd pobierania haseł", "details": str(e)}), 500


@passwords_bp.route("/", methods=["POST"])
@jwt_required()
def add_password():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        site = safe_encrypt(data.get("site", ""))
        login = safe_encrypt(data.get("login", ""))
        password = safe_encrypt(data.get("password", ""))
        notes = safe_encrypt(data.get("notes", ""))

        new_entry = StoredPassword(
            user_id=user_id,
            site=site,
            login=login,
            password=password,
            notes=notes
        )

        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Hasło zostało zapisane."}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd podczas dodawania hasła", "details": str(e)}), 500


@passwords_bp.route("/<int:password_id>", methods=["DELETE"])
@jwt_required()
def delete_password(password_id):
    try:
        user_id = get_jwt_identity()
        password_entry = StoredPassword.query.filter_by(id=password_id, user_id=user_id).first()

        if not password_entry:
            return jsonify({"error": "Nie znaleziono hasła."}), 404

        db.session.delete(password_entry)
        db.session.commit()
        return jsonify({"message": "Hasło zostało usunięte."})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd podczas usuwania hasła", "details": str(e)}), 500


@passwords_bp.route("/<int:password_id>", methods=["PUT"])
@jwt_required()
def update_password(password_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        password_entry = StoredPassword.query.filter_by(id=password_id, user_id=user_id).first()
        if not password_entry:
            return jsonify({"error": "Nie znaleziono hasła."}), 404

        # Szyfrujemy dane przy aktualizacji
        if "site" in data:
            password_entry.site = safe_encrypt(data["site"])
        if "login" in data:
            password_entry.login = safe_encrypt(data["login"])
        if "password" in data:
            password_entry.password = safe_encrypt(data["password"])
        if "notes" in data:
            password_entry.notes = safe_encrypt(data["notes"])

        db.session.commit()
        return jsonify({"message": "Hasło zostało zaktualizowane."})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Błąd aktualizacji hasła", "details": str(e)}), 500
