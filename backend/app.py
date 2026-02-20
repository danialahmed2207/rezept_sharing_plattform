"""
Einfache Rezept API mit Flask und SQLite
"""

import sqlite3
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mein-geheimer-schluessel'

# Datenbank-Verbindung
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Tabellen erstellen
def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            steps TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    db.commit()

# Login-Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({'error': 'Nicht eingeloggt'}), 401
        # Einfache Auth-Check (nur fürs Demo)
        return f(*args, **kwargs)
    return decorated_function

# ========== ROUTES ==========

@app.route('/')
def home():
    return jsonify({'message': 'Rezept API läuft!'})

# Registrierung
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username und Passwort nötig'}), 400
    
    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return jsonify({'message': 'User erstellt'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username existiert schon'}), 400

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    
    if user and check_password_hash(user['password'], password):
        return jsonify({
            'message': 'Login erfolgreich',
            'user_id': user['id'],
            'username': user['username']
        })
    return jsonify({'error': 'Falsche Daten'}), 401

# Alle Rezepte anzeigen
@app.route('/recipes', methods=['GET'])
def get_recipes():
    db = get_db()
    recipes = db.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
    return jsonify({
        'recipes': [dict(recipe) for recipe in recipes]
    })

# Ein Rezept anzeigen
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    db = get_db()
    recipe = db.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    if recipe:
        return jsonify(dict(recipe))
    return jsonify({'error': 'Rezept nicht gefunden'}), 404

# Rezept erstellen
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    title = data.get('title')
    ingredients = data.get('ingredients')
    steps = data.get('steps')
    user_id = data.get('user_id', 1)  # Default user für Demo
    
    if not title or not ingredients or not steps:
        return jsonify({'error': 'Alle Felder nötig'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO recipes (title, ingredients, steps, user_id) VALUES (?, ?, ?, ?)',
        (title, ingredients, steps, user_id)
    )
    db.commit()
    
    return jsonify({
        'message': 'Rezept erstellt',
        'id': cursor.lastrowid
    }), 201

# Rezept aktualisieren
@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.get_json()
    title = data.get('title')
    ingredients = data.get('ingredients')
    steps = data.get('steps')
    
    # Prüfen ob Rezept existiert
    db = get_db()
    recipe = db.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    if not recipe:
        return jsonify({'error': 'Rezept nicht gefunden'}), 404
    
    db.execute(
        'UPDATE recipes SET title=?, ingredients=?, steps=? WHERE id=?',
        (title, ingredients, steps, id)
    )
    db.commit()
    return jsonify({'message': 'Rezept aktualisiert'})

# Rezept löschen
@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    db = get_db()
    db.execute('DELETE FROM recipes WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Rezept gelöscht'})

# Server starten
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, port=5000)
