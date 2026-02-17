from flask import Blueprint, g, jsonify, request

from .db import get_db
from .security import token_required

recipes_bp = Blueprint("recipes", __name__, url_prefix="/api/recipes")


def _fetch_recipe(db, recipe_id):
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
    db = get_db()
    recipe = _fetch_recipe(db, recipe_id)
    if recipe is None:
        return jsonify({"error": "Rezept nicht gefunden"}), 404
    return jsonify({"recipe": dict(recipe)})


@recipes_bp.post("")
@token_required
def create_recipe():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    ingredients = data.get("ingredients", "").strip()
    steps = data.get("steps", "").strip()

    if not title or not ingredients or not steps:
        return jsonify({"error": "title, ingredients, steps sind Pflicht"}), 400

    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO recipes (user_id, title, ingredients, steps)
        VALUES (?, ?, ?, ?)
        """,
        (g.current_user["id"], title, ingredients, steps),
    )
    db.commit()

    recipe = _fetch_recipe(db, cursor.lastrowid)
    return jsonify({"message": "Rezept erstellt", "recipe": dict(recipe)}), 201


@recipes_bp.put("/<int:recipe_id>")
@token_required
def update_recipe(recipe_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    ingredients = data.get("ingredients", "").strip()
    steps = data.get("steps", "").strip()

    if not title or not ingredients or not steps:
        return jsonify({"error": "title, ingredients, steps sind Pflicht"}), 400

    db = get_db()
    recipe = db.execute(
        "SELECT id, user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    ).fetchone()
    if recipe is None:
        return jsonify({"error": "Rezept nicht gefunden"}), 404
    if recipe["user_id"] != g.current_user["id"]:
        return jsonify({"error": "Nur der Owner darf aendern"}), 403

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
    db = get_db()
    recipe = db.execute(
        "SELECT id, user_id FROM recipes WHERE id = ?",
        (recipe_id,),
    ).fetchone()
    if recipe is None:
        return jsonify({"error": "Rezept nicht gefunden"}), 404
    if recipe["user_id"] != g.current_user["id"]:
        return jsonify({"error": "Nur der Owner darf loeschen"}), 403

    db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()
    return jsonify({"message": "Rezept geloescht"})
