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
    app = Flask(__name__)

    backend_root = Path(__file__).resolve().parent.parent
    load_dotenv(backend_root / ".env")

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev_secret_key_change_me"),
        DATABASE=str(backend_root / "database.db"),
    )

    if test_config:
        app.config.update(test_config)

    CORS(app)
    init_db(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(favorites_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app
