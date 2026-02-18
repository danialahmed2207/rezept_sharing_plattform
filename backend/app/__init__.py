"""
Flask Anwendungs-Factory fuer die Rezept Sharing Plattform.

Dieses Modul erstellt und konfiguriert die Flask-App mit:
- Datenbank-Anbindung (SQLite)
- CORS fuer Cross-Origin Requests
- Blueprint-Registrierung fuer alle API-Routen
"""

import os
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .db import init_app as init_db
from .routes_auth import auth_bp
from .routes_comments import comments_bp
from .routes_favorites import favorites_bp
from .routes_recipes import recipes_bp


def create_app(test_config=None):
    """
    Erstellt und konfiguriert die Flask-Anwendung.
    
    Args:
        test_config: Optionale Test-Konfiguration fuer Unit-Tests
        
    Returns:
        Flask: Die konfigurierte Flask-Anwendung
    """
    app = Flask(__name__)

    # Backend-Verzeichnis ermitteln
    backend_root = Path(__file__).resolve().parent.parent
    
    # Umgebungsvariablen aus .env laden
    load_dotenv(backend_root / ".env")

    # Standard-Konfiguration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev_secret_key_change_me"),
        DATABASE=str(backend_root / "database.db"),
    )

    # Test-Konfiguration ueberschreibt Standard
    if test_config:
        app.config.update(test_config)

    # CORS aktivieren (fuer Frontend-Zugriff)
    CORS(app)
    
    # Datenbank initialisieren
    init_db(app)

    # Blueprints registrieren
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(favorites_bp)

    # Health-Check Endpoint
    @app.get("/api/health")
    def health():
        """Gibt den Status der API zurueck."""
        return jsonify({"status": "ok"})

    return app
