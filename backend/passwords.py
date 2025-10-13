from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import StoredPassword
from encryption_utils import encrypt_text, decrypt_text


passwords_bp = Blueprint("passwords", __name__)


@passwords_bp.route("/", methods=["GET"])
@jwt_required()
def list_passwords():
    user_id = user_id = int(get_jwt_identity())
    try:
        rows = StoredPassword.query.filter_by(user_id=user_id).all()
        out = []
        for r in rows:
            try:
                pwd = decrypt_text(r.password)
            except Exception:
                pwd = r.password
            out.append({
                "id": r.id,
                "site": r.site,
                "login": r.login,
                "password": pwd,
                "notes": r.notes or "",
            })
        return jsonify(out), 200
    except Exception as e:
        print("Błąd GET /api/passwords/:", e)
        return jsonify({"error": "Błąd pobierania haseł"}), 500


@passwords_bp.route("/", methods=["POST"])
@jwt_required()
def add_password():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    site = (data.get("site") or "").strip()
    login = (data.get("login") or "").strip()
    password = data.get("password") or ""
    notes = data.get("notes") or ""

    if not site or not login or not password:
        return jsonify({"error": "Brakujące pola (strona, login, hasło)."}), 400

    try:
        enc = encrypt_text(password)
    except Exception:
        enc = password

    try:
        entry = StoredPassword(
            user_id=user_id,
            site=site,
            login=login,
            password=enc,
            notes=notes
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({"message": "Zapisano", "id": entry.id}), 201
    except Exception as e:
        print("Błąd zapisu hasła:", e)
        db.session.rollback()
        return jsonify({"error": "Błąd zapisu hasła"}), 500


@passwords_bp.route("/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_password(entry_id):
    user_id = int(get_jwt_identity())
    entry = StoredPassword.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Nie znaleziono lub brak uprawnień."}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Usunięto."}), 200


@passwords_bp.route("/<int:entry_id>", methods=["PUT"])
@jwt_required()
def update_password(entry_id):
    user_id = int(get_jwt_identity())
    entry = StoredPassword.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Nie znaleziono lub brak uprawnień."}), 404

    data = request.get_json(silent=True) or {}

    if "site" in data:
        entry.site = data["site"]
    if "login" in data:
        entry.login = data["login"]
    if "password" in data:
        try:
            entry.password = encrypt_text(data["password"])
        except Exception:
            entry.password = data["password"]
    if "notes" in data:
        entry.notes = data["notes"]

    db.session.commit()
    return jsonify({"message": "Zaktualizowano."}), 200
