"""
Rezept-Routen fuer die Rezept Sharing Plattform.

Endpunkte:
- GET /api/recipes - Alle Rezepte auflisten
- GET /api/recipes/<id> - Einzelnes Rezept anzeigen
- POST /api/recipes - Rezept erstellen (Auth)
- PUT /api/recipes/<id> - Rezept aktualisieren (Auth, Owner)
- DELETE /api/recipes/<id> - Rezept loeschen (Auth, Owner)
"""

from flask import Blueprint, g, jsonify, request

from .db import get_db
from .security import token_required

recipes_bp = Blueprint("recipes", __name__, url_prefix="/api/recipes")


def _fetch_recipe(db, recipe_id):
    """
    Hilfsfunktion: Laedt ein Rezept mit Zusatzinformationen.
    
    Args:
        db: Datenbankverbindung
        recipe_id: ID des Rezepts
        
    Returns:
        sqlite3.Row oder None: Das Rezept oder None wenn nicht gefunden
    """
    return db.execute(
        """
        SELECT
            r.id,
            r.title,
            r.ingredients,
            r.steps,
            r.created_at,
            r.updated_at,
            r.user_id AS owner_id,
            u.username AS owner_username,
            (SELECT COUNT(*) FROM comments c WHERE c.recipe_id = r.id) AS comment_count,
            (SELECT COUNT(*) FROM favorites f WHERE f.recipe_id = r.id) AS favorite_count
        FROM recipes r
        JOIN users u ON u.id = r.user_id
        WHERE r.id = ?
        """,
        (recipe_id,),
    ).fetchone()


@recipes_bp.get("")
def list_recipes():
    """
    Listet alle Rezepte auf (neueste zuerst).
    
    Returns:
        200: Liste aller Rezepte
    """
    db = get_db()
    rows = db.execute(
        """
        SELECT
            r.id,
            r.title,
            r.ingredients,
            r.steps,
            r.created_at,
            r.updated_at,
            r.user_id AS owner_id,
            u.username AS owner_username,
            (SELECT COUNT(*) FROM comments c WHERE c.recipe_id = r.id) AS comment_count,
            (SELECT COUNT(*) FROM favorites f WHERE f.recipe_id = r.id) AS favorite_count
        FROM recipes r
        JOIN users u ON u.id = r.user_id
        ORDER BY r.created_at DESC
        """
    ).fetchall()
    return jsonify({"recipes": [dict(row) for row in rows]})


@recipes_bp.get("/<int:recipe_id>")
def get_recipe(recipe_id):
    """
    Zeigt ein einzelnes Rezept an.
    
    Args:
        recipe_id: ID des Rezepts
        
    Returns:
        200: Rezeptdaten
        404: Rezept nicht gefunden
    """
    db = get_db()
    recipe = _fetch_recipe(db, recipe_id)
    if recipe is None:
        return jsonify({"error": "Rezept nicht gefunden"}), 404
    return jsonify({"recipe": dict(recipe)})


@recipes_bp.post("")
@token_required
def create_recipe():
    """
    Erstellt ein neues Rezept.
    
    Header:
        - Authorization: Bearer <token>
        
    Erforderliche Felder:
        - title: Titel des Rezepts
        - ingredients: Zutaten
        - steps: Zubereitungsschritte
        
    Returns:
        201: Rezept erstellt
        400: Fehlende Daten
        401: Nicht eingeloggt
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    ingredients = data.get("ingredients", "").strip()
    steps = data.get("steps", "").strip()

    # Validierung
    if not title or not ingredients or not steps:
        return jsonify({"error": "Titel, Zutaten und Zubereitung sind Pflicht"}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO recipes (user_id, title, ingredients, steps) VALUES (?, ?, ?, ?)",
        (g.current_user["id"], title, ingredients, steps),
    )
    db.commit()

    recipe = _fetch_recipe(db, cursor.lastrowid)
    return jsonify({"message": "Rezept erstellt", "recipe": dict(recipe)}), 201


@recipes_bp.put("/<int:recipe_id>")
@token_required
def update_recipe(recipe_id):
    """
    Aktualisiert ein eigenes Rezept.
    
    Header:
        - Authorization: Bearer <token>
        
    Args:
        recipe_id: ID des Rezepts
        
    Returns:
        200: Rezept aktualisiert
        400: Fehlende Daten
        403: Keine Berechtigung (nicht Owner)
        404: Rezept nicht gefunden
    """
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    ingredients = data.get("ingredients", "").strip()
    steps = data.get("steps", "").strip()

    # Validierung
    if not title or not ingredients or not steps:
        return jsonify({"error": "Titel, Zutaten und Zubereitung sind Pflicht"}), 400

    db = get_db()
    
    # Rezept suchen
    recipe = db.execute(
        "SELECT id, user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    ).fetchone()
    
    if recipe is None:
        return jsonify({"error": "Rezept nicht gefunden"}), 404
    
    # Berechtigung pruefen
    if recipe["user_id"] != g.current_user["id"]:
        return jsonify({"error": "Nur der Ersteller darf das Rezept aendern"}), 403

    # Rezept aktualisieren
    db.execute(
        """
        UPDATE recipes
        SET title = ?, ingredients = ?, steps = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (title, ingredients, steps, recipe_id),
    )
    db.commit()

    updated_recipe = _fetch_recipe(db, recipe_id)
    return jsonify({"message": "Rezept aktualisiert", "recipe": dict(updated_recipe)})


@recipes_bp.delete("/<int:recipe_id>")
@token_required
def delete_recipe(recipe_id):
    """
    Loescht ein eigenes Rezept.
    
    Header:
        - Authorization: Bearer <token>
        
    Args:
        recipe_id: ID des Rezepts
        
    Returns:
        200: Rezept geloescht
        403: Keine Berechtigung (nicht Owner)
        404: Rezept nicht gefunden
    """
    db = get_db()
    
    # Rezept suchen
    recipe = db.execute(
        "SELECT id, user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    ).fetchone()
    
    if recipe is None:
        return jsonify({"error": "Rezept nicht gefunden"}), 404
    
    # Berechtigung pruefen
    if recipe["user_id"] != g.current_user["id"]:
        return jsonify({"error": "Nur der Ersteller darf das Rezept loeschen"}), 403

    # Rezept loeschen
    db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
    return jsonify({"message": "Rezept geloescht"})
