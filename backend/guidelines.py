from flask import Blueprint, jsonify


guidelines_bp = Blueprint("guidelines_bp", __name__)


@guidelines_bp.route("/guidelines")
def get_guidelines():
    return jsonify({
        "Cyberbezpieczeństwo": [
            "Placeholder cyberbezpieczeństwo 1.",
            "Placeholder cyberbezpieczeństwo 2.",
            "Placeholder cyberbezpieczeństwo 3."
        ],
        "Bezpieczne Hasła": [
            "Placeholder bezpieczne hasła 1.",
            "Placeholder bezpieczne hasła 2.",
            "Placeholder bezpieczne hasła 3."
        ],
        "Uwierzytelnianie": [
            "Placeholder uwierzytelnianie 1.",
            "Placeholder uwierzytelnianie 2.",
            "Placeholder uwierzytelnianie 3."
        ],
        "Ataki na Użytkowników": [
            "Placeholder ataki 1.",
            "Placeholder ataki 2.",
            "Placeholder ataki 3."
        ]
    })
