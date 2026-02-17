from flask import Blueprint, g, jsonify, request

from .db import get_db
from .security import create_token, hash_password, token_required, verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "Benutzername, E-Mail und Passwort sind Pflicht"}), 400
    if len(password) < 6:
        return jsonify({"error": "Passwort muss mindestens 6 Zeichen haben"}), 400

    db = get_db()
    existing_user = db.execute(
        "SELECT id FROM users WHERE email = ? OR username = ?",
        (email, username),
    ).fetchone()
    if existing_user:
        return jsonify({"error": "Benutzername oder E-Mail existiert bereits"}), 409

    db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, hash_password(password)),
    )
    db.commit()

    new_user = db.execute(
        "SELECT id, username, email FROM users WHERE email = ?",
        (email,),
    ).fetchone()

    return (
        jsonify(
            {
                "message": "Registrierung erfolgreich",
                "user": dict(new_user),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "E-Mail und Passwort sind Pflicht"}), 400

    db = get_db()
    user = db.execute(
        "SELECT id, username, email, password_hash FROM users WHERE email = ?",
        (email,),
    ).fetchone()

    if user is None or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Login fehlgeschlagen"}), 401

    token = create_token(user["id"])
    return jsonify(
        {
            "message": "Login erfolgreich",
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
            },
        }
    )


@auth_bp.get("/me")
@token_required
def me():
    return jsonify({"user": g.current_user})
