from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import StoredPassword
from encryption_utils import encrypt_text, decrypt_text
import re


passwords_bp = Blueprint("passwords_bp", __name__)


@passwords_bp.route("/", methods=["GET"])
@jwt_required()
def get_passwords():
    user_id = int(get_jwt_identity())

    try:
        passwords = StoredPassword.query.filter_by(user_id=user_id).all()
        data = []
        for p in passwords:
            try:
                decrypted = decrypt_text(p.password)
            except Exception:
                decrypted = "[BŁĄD ODSZYFROWANIA]"
            data.append({
                "id": p.id,
                "site": p.site,
                "login": p.login,
                "password": decrypted,
                "notes": p.notes or ""
            })
        return jsonify(data), 200
    except Exception as e:
        import traceback 
        traceback.print_exc()
        return jsonify({"error": "Błąd pobierania haseł"}), 500


@passwords_bp.route("/", methods=["POST"])
@jwt_required()
def add_password():
    user_id = int(get_jwt_identity())
    try:
        data = request.get_json(force=True)
    except Exception as e:
        print("Błąd parsowania JSON:", e)
        return jsonify({"error": "Niepoprawne dane JSON"}), 400

    site = (data.get("site") or "").strip()
    login = (data.get("login") or "").strip()
    password = (data.get("password") or "").strip()
    notes = (data.get("notes") or "").strip()

    if not site or not login or not password:
        return jsonify({"error": "Wymagane pola: site, login, password"}), 400

    if len(site) > 255 or len(login) > 255 or len(password) > 1024 or len(notes) > 1024:
        return jsonify({"error": "Dane wejściowe są zbyt długie."}), 400

    site = re.sub(r"[^a-zA-Z0-9.\-_/]", "", site)

    try:
        encrypted_password = encrypt_text(password)
    except Exception as e:
        print("Błąd szyfrowania:", e)
        encrypted_password = password

    try:
        entry = StoredPassword(
            user_id=user_id,
            site=site,
            login=login,
            password=encrypted_password,
            notes=notes
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({"message": "Hasło zapisane pomyślnie", "id": entry.id}), 201
    except Exception as e:
        print("Błąd zapisu hasła:", e)
        db.session.rollback()
        return jsonify({"error": "Błąd zapisu hasła"}), 500


@passwords_bp.route("/<int:pw_id>", methods=["DELETE"])
@jwt_required()
def delete_password(pw_id):
    user_id = int(get_jwt_identity())
    try:
        entry = StoredPassword.query.filter_by(id=pw_id, user_id=user_id).first()
        if not entry:
            return jsonify({"error": "Nie znaleziono wpisu"}), 404
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": "Usunięto"}), 200
    except Exception as e:
        print("Błąd DELETE:", e)
        db.session.rollback()
        return jsonify({"error": "Błąd usuwania"}), 500


@passwords_bp.route("/<int:pw_id>", methods=["PUT"])
@jwt_required()
def update_password(pw_id):
    user_id = int(get_jwt_identity())
    entry = StoredPassword.query.filter_by(id=pw_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Nie znaleziono lub brak uprawnień."}), 404

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Niepoprawny JSON"}), 400

    if "site" in data:
        entry.site = data["site"].strip()
    if "login" in data:
        entry.login = data["login"].strip()
    if "password" in data:
        try:
            entry.password = encrypt_text(data["password"])
        except Exception:
            entry.password = data["password"]
    if "notes" in data:
        entry.notes = data["notes"].strip()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Błąd aktualizacji hasła: {type(e).__name__}")
        return jsonify({"error": "Błąd podczas aktualizacji"}), 500

    return jsonify({"message": "Hasło zaktualizowano."}), 200