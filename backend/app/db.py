"""
Datenbank-Modul fuer die Rezept Sharing Plattform.

Verwendet SQLite mit:
- Verbindungs-Management (get_db, close_db)
- Automatische Tabellen-Erstellung
- Foreign Key Support
"""

import sqlite3

from flask import current_app, g

# SQL-Schema fuer alle Tabellen
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    steps TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);
"""


def get_db():
    """
    Gibt die aktuelle Datenbankverbindung zurueck.
    
    Erstellt eine neue Verbindung, falls noch keine existiert.
    Aktiviert Foreign Keys und Row-Factory fuer Dictionary-Zugriff.
    
    Returns:
        sqlite3.Connection: Die Datenbankverbindung
    """
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"])
        connection.row_factory = sqlite3.Row  # Dictionary-Zugriff ermoeglichen
        connection.execute("PRAGMA foreign_keys = ON")  # Foreign Keys aktivieren
        g.db = connection
    return g.db


def close_db(_error=None):
    """
    Schliesst die Datenbankverbindung.
    
    Wird automatisch am Ende eines Requests aufgerufen.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """
    Initialisiert die Datenbank mit dem Schema.
    
    Erstellt alle Tabellen, falls sie nicht existieren.
    """
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()


def init_app(app):
    """
    Registriert Datenbank-Funktionen bei der Flask-App.
    
    Args:
        app: Die Flask-Anwendung
    """
    # Datenbankverbindung am Ende jedes Requests schliessen
    app.teardown_appcontext(close_db)
    
    # Tabellen erstellen
    with app.app_context():
        init_db()
