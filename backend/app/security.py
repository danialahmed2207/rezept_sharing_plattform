from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def token_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token fehlt"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        payload = decode_token(token)
        if not payload or "user_id" not in payload:
            return jsonify({"error": "Ungueltiger Token"}), 401

        db = get_db()
        user = db.execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (payload["user_id"],),
        ).fetchone()

        if user is None:
            return jsonify({"error": "Benutzer nicht gefunden"}), 401

        g.current_user = dict(user)
        return view_func(*args, **kwargs)

    return wrapped
