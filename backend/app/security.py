"""
Sicherheits-Modul fuer die Rezept Sharing Plattform.

Bietet:
- Passwort-Hashing mit Werkzeug
- JWT-Token Erstellung und Validierung
- Decorator fuer geschuetzte Routen
"""

from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


def hash_password(password):
    """
    Hasht ein Passwort sicher.
    
    Args:
        password: Das Klartext-Passwort
        
    Returns:
        str: Der Passwort-Hash
    """
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """
    Prueft ein Passwort gegen einen Hash.
    
    Args:
        password: Das Klartext-Passwort
        password_hash: Der gespeicherte Hash
        
    Returns:
        bool: True wenn das Passwort stimmt
    """
    return check_password_hash(password_hash, password)


def create_token(user_id):
    """
    Erstellt einen JWT-Token fuer einen Benutzer.
    
    Der Token ist 24 Stunden gueltig.
    
    Args:
        user_id: Die ID des Benutzers
        
    Returns:
        str: Der JWT-Token
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    """
    Dekodiert und validiert einen JWT-Token.
    
    Args:
        token: Der JWT-Token
        
    Returns:
        dict oder None: Das Token-Payload oder None bei Fehler
    """
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def token_required(view_func):
    """
    Decorator fuer geschuetzte API-Endpunkte.
    
    Prueft den Authorization-Header und laedt den Benutzer.
    Der Benutzer ist dann in g.current_user verfuegbar.
    
    Args:
        view_func: Die zu schuetzende Funktion
        
    Returns:
        function: Die geschuetzte Funktion
    """
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        # Authorization-Header pruefen
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token fehlt"}), 401

        # Token extrahieren und validieren
        token = auth_header.split(" ", 1)[1].strip()
        payload = decode_token(token)
        if not payload or "user_id" not in payload:
            return jsonify({"error": "Ungueltiger Token"}), 401

        # Benutzer aus Datenbank laden
        db = get_db()
        user = db.execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (payload["user_id"],),
        ).fetchone()

        if user is None:
            return jsonify({"error": "Benutzer nicht gefunden"}), 401

        # Benutzer in Flask's g-Objekt speichern
        g.current_user = dict(user)
        return view_func(*args, **kwargs)

    return wrapped
