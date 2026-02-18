from flask import Blueprint, g, jsonify

from .db import get_db
from .security import token_required

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api")


def _recipe_exists(db, recipe_id):
    recipe = db.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    return recipe is not None


@favorites_bp.post("/recipes/<int:recipe_id>/favorite")
@token_required
def add_favorite(recipe_id):
    db = get_db()
    if not _recipe_exists(db, recipe_id):
        return jsonify({"error": "Rezept nicht gefunden"}), 404

    existing = db.execute(
        "SELECT id FROM favorites WHERE user_id = ? AND recipe_id = ?",
        (g.current_user["id"], recipe_id),
    ).fetchone()
    if existing:
        return jsonify({"message": "Rezept ist bereits Favorit"})

    db.execute(
        "INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)",
        (g.current_user["id"], recipe_id),
    )
    db.commit()
    return jsonify({"message": "Favorit hinzugefuegt"}), 201


@favorites_bp.delete("/recipes/<int:recipe_id>/favorite")
@token_required
def remove_favorite(recipe_id):
    db = get_db()
    
    # Pruefen ob Favorit existiert
    existing = db.execute(
        "SELECT id FROM favorites WHERE user_id = ? AND recipe_id = ?",
        (g.current_user["id"], recipe_id),
    ).fetchone()
    
    if not existing:
        return jsonify({"error": "Favorit nicht gefunden"}), 404
    
    db.execute(
        "DELETE FROM favorites WHERE user_id = ? AND recipe_id = ?",
        (g.current_user["id"], recipe_id),
    )
    db.commit()
    return jsonify({"message": "Favorit entfernt"})


@favorites_bp.get("/favorites")
@token_required
def list_favorites():
    db = get_db()
    rows = db.execute(
        """
        SELECT
            f.id AS favorite_id,
            f.created_at AS favorited_at,
            r.id AS recipe_id,
            r.title,
            r.ingredients,
            r.steps,
            u.username AS owner_username
        FROM favorites f
        JOIN recipes r ON r.id = f.recipe_id
        JOIN users u ON u.id = r.user_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
        """,
        (g.current_user["id"],),
    ).fetchall()
    return jsonify({"favorites": [dict(row) for row in rows]})
