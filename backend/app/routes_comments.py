from flask import Blueprint, g, jsonify, request

from .db import get_db
from .security import token_required

comments_bp = Blueprint("comments", __name__, url_prefix="/api")


def _recipe_exists(db, recipe_id):
    recipe = db.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    return recipe is not None


@comments_bp.get("/recipes/<int:recipe_id>/comments")
def list_comments(recipe_id):
    db = get_db()
    if not _recipe_exists(db, recipe_id):
        return jsonify({"error": "Rezept nicht gefunden"}), 404

    rows = db.execute(
        """
        SELECT
            c.id,
            c.recipe_id,
            c.user_id,
            c.content,
            c.created_at,
            u.username
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.recipe_id = ?
        ORDER BY c.created_at DESC
        """,
        (recipe_id,),
    ).fetchall()
    return jsonify({"comments": [dict(row) for row in rows]})


@comments_bp.post("/recipes/<int:recipe_id>/comments")
@token_required
def create_comment(recipe_id):
    db = get_db()
    if not _recipe_exists(db, recipe_id):
        return jsonify({"error": "Rezept nicht gefunden"}), 404

    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "content ist Pflicht"}), 400

    cursor = db.execute(
        """
        INSERT INTO comments (recipe_id, user_id, content)
        VALUES (?, ?, ?)
        """,
        (recipe_id, g.current_user["id"], content),
    )
    db.commit()

    comment = db.execute(
        """
        SELECT
            c.id,
            c.recipe_id,
            c.user_id,
            c.content,
            c.created_at,
            u.username
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.id = ?
        """,
        (cursor.lastrowid,),
    ).fetchone()

    return jsonify({"message": "Kommentar erstellt", "comment": dict(comment)}), 201


@comments_bp.put("/comments/<int:comment_id>")
@token_required
def update_comment(comment_id):
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "content ist Pflicht"}), 400

    db = get_db()
    comment = db.execute(
        "SELECT id, user_id FROM comments WHERE id = ?",
        (comment_id,),
    ).fetchone()
    if comment is None:
        return jsonify({"error": "Kommentar nicht gefunden"}), 404
    if comment["user_id"] != g.current_user["id"]:
        return jsonify({"error": "Nur der Owner darf aendern"}), 403

    db.execute(
        "UPDATE comments SET content = ? WHERE id = ?",
        (content, comment_id),
    )
    db.commit()

    updated_comment = db.execute(
        """
        SELECT
            c.id,
            c.recipe_id,
            c.user_id,
            c.content,
            c.created_at,
            u.username
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.id = ?
        """,
        (comment_id,),
    ).fetchone()
    return jsonify({"message": "Kommentar aktualisiert", "comment": dict(updated_comment)})


@comments_bp.delete("/comments/<int:comment_id>")
@token_required
def delete_comment(comment_id):
    db = get_db()
    comment = db.execute(
        "SELECT id, user_id FROM comments WHERE id = ?",
        (comment_id,),
    ).fetchone()
    if comment is None:
        return jsonify({"error": "Kommentar nicht gefunden"}), 404
    if comment["user_id"] != g.current_user["id"]:
        return jsonify({"error": "Nur der Owner darf loeschen"}), 403

    db.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    db.commit()
    return jsonify({"message": "Kommentar geloescht"})
