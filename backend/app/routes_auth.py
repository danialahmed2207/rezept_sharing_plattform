"""
Authentifizierungs-Routen fuer die Rezept Sharing Plattform.

Endpunkte:
- POST /api/auth/register - Benutzer registrieren
- POST /api/auth/login - Benutzer anmelden
- GET /api/auth/me - Aktuellen Benutzer abfragen
"""

from flask import Blueprint, g, jsonify, request

from .db import get_db
from .security import create_token, hash_password, token_required, verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    """
    Registriert einen neuen Benutzer.
    
    Erforderliche Felder:
        - username: Benutzername (eindeutig)
        - email: E-Mail-Adresse (eindeutig)
        - password: Passwort (mindestens 6 Zeichen)
        
    Returns:
        201: Benutzer wurde erstellt
        400: Fehlende oder ungueltige Daten
        409: Benutzername oder E-Mail existiert bereits
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validierung
    if not username or not email or not password:
        return jsonify({"error": "Benutzername, E-Mail und Passwort sind Pflicht"}), 400
    if len(password) < 6:
        return jsonify({"error": "Passwort muss mindestens 6 Zeichen haben"}), 400

    db = get_db()
    
    # Pruefen ob Benutzer bereits existiert
    existing_user = db.execute(
        "SELECT id FROM users WHERE email = ? OR username = ?",
        (email, username),
    ).fetchone()
    if existing_user:
        return jsonify({"error": "Benutzername oder E-Mail existiert bereits"}), 409

    # Benutzer erstellen
    db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, hash_password(password)),
    )
    db.commit()

    # Neuen Benutzer zurueckgeben
    new_user = db.execute(
        "SELECT id, username, email FROM users WHERE email = ?",
        (email,),
    ).fetchone()

    return (
        jsonify({
            "message": "Registrierung erfolgreich",
            "user": dict(new_user),
        }),
        201,
    )


@auth_bp.post("/login")
def login():
    """
    Meldet einen Benutzer an.
    
    Erforderliche Felder:
        - email: E-Mail-Adresse
        - password: Passwort
        
    Returns:
        200: Login erfolgreich (mit Token)
        400: Fehlende Daten
        401: Falsche Anmeldedaten
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validierung
    if not email or not password:
        return jsonify({"error": "E-Mail und Passwort sind Pflicht"}), 400

    db = get_db()
    
    # Benutzer suchen
    user = db.execute(
        "SELECT id, username, email, password_hash FROM users WHERE email = ?",
        (email,),
    ).fetchone()

    # Passwort pruefen
    if user is None or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Login fehlgeschlagen"}), 401

    # Token erstellen
    token = create_token(user["id"])
    return jsonify({
        "message": "Login erfolgreich",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        },
    })


@auth_bp.get("/me")
@token_required
def me():
    """
    Gibt den aktuell eingeloggten Benutzer zurueck.
    
    Header:
        - Authorization: Bearer <token>
        
    Returns:
        200: Benutzerdaten
        401: Ungueltiger oder fehlender Token
    """
    return jsonify({"user": g.current_user})
