from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import StoredPassword
from encryption_utils import encrypt_text, decrypt_text


passwords_bp = Blueprint("passwords", __name__)


@passwords_bp.route("/", methods=["GET"])
@jwt_required()
def list_passwords():
    user_id = get_jwt_identity()
    rows = StoredPassword.query.filter_by(user_id=user_id).order_by(StoredPassword.created_at.desc()).all()
    out = []

    for r in rows:
        try:
            pwd = decrypt_text(r.password_encrypted)
        except Exception:
            pwd = r.password_encrypted
        out.append({
            "id": r.id,
            "site": r.site,
            "login": r.login,
            "password": pwd,
            "notes": r.notes,
            "created_at": r.created_at.isoformat()
        })
    return jsonify(out), 200


@passwords_bp.route("/", methods=["POST"])
@jwt_required()
def add_password():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    site = (data.get("site") or "").strip()
    login = (data.get("login") or "").strip()
    password = data.get("password") or ""
    notes = data.get("notes") or ""

    if not site or not login or not password:
        return jsonify({"error": "Brakujące pola (strona, login, hasło)."}), 400

    enc = encrypt_text(password)
    entry = StoredPassword(site=site, login=login, password_encrypted=enc, notes=notes, user_id=user_id)
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Zapisano", "id": entry.id}), 201


@passwords_bp.route("/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_password(entry_id):
    user_id = get_jwt_identity()
    entry = StoredPassword.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Nie znaleziono lub nieautoryzowano."}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Usunięto."}), 200


@passwords_bp.route("/<int:entry_id>", methods=["PUT"])
@jwt_required()
def update_password(entry_id):
    user_id = get_jwt_identity()
    entry = StoredPassword.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({"error": "Nie znaleziono lub nieautoryzowano."}), 404
    data = request.get_json() or {}
    if "site" in data: entry.site = data["site"]
    if "login" in data: entry.login = data["login"]
    if "password" in data: entry.password_encrypted = encrypt_text(data["password"])
    if "notes" in data: entry.notes = data["notes"]
    db.session.commit()
    return jsonify({"message": "Updated"}), 200
