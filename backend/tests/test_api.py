"""
API Tests fuer die Rezept Sharing Plattform.

Diese Tests pruefen:
- Health Check
- Benutzer-Registrierung (Erfolg & Fehler)
- Login (Erfolg & Fehler)
- Rezepte CRUD (Erfolg & Fehler)
- Kommentare (Erfolg & Fehler)
- Favoriten (Erfolg & Fehler)

Ausfuehren:
    cd backend
    python -m unittest discover -s tests -v
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app import create_app


class ApiTestCase(unittest.TestCase):
    """Test-Klasse fuer API-Endpunkte."""

    def setUp(self):
        """Vor jedem Test: Temporaere Datenbank erstellen."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": self.db_path,
                "SECRET_KEY": "test_secret",
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        """Nach jedem Test: Temporaere Datenbank loeschen."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _register_user(self, username="testuser", email="test@example.com", password="passwort123"):
        """Hilfsfunktion: Benutzer registrieren."""
        return self.client.post(
            "/api/auth/register",
            json={"username": username, "email": email, "password": password},
        )

    def _login_user(self, email="test@example.com", password="passwort123"):
        """Hilfsfunktion: Benutzer einloggen und Token zurueckgeben."""
        response = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            return response.get_json()["token"]
        return None

    def test_health_check(self):
        """Test: Health-Check Endpoint."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")

    # ==================== AUTH TESTS ====================

    def test_register_success(self):
        """Test: Erfolgreiche Registrierung."""
        response = self._register_user()
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["user"]["username"], "testuser")
        self.assertEqual(data["user"]["email"], "test@example.com")

    def test_register_duplicate_email(self):
        """Test: Registrierung mit doppelter E-Mail."""
        self._register_user()
        response = self._register_user(username="anderer", email="test@example.com")
        self.assertEqual(response.status_code, 409)
        self.assertIn("existiert bereits", response.get_json()["error"])

    def test_register_duplicate_username(self):
        """Test: Registrierung mit doppeltem Benutzernamen."""
        self._register_user()
        response = self._register_user(username="testuser", email="anderer@example.com")
        self.assertEqual(response.status_code, 409)
        self.assertIn("existiert bereits", response.get_json()["error"])

    def test_register_validation(self):
        """Test: Registrierung mit fehlenden Daten."""
        # Fehlende Daten
        response = self.client.post(
            "/api/auth/register",
            json={"username": "test"},
        )
        self.assertEqual(response.status_code, 400)

        # Zu kurzes Passwort
        response = self.client.post(
            "/api/auth/register",
            json={"username": "test", "email": "test@example.com", "password": "123"},
        )
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        """Test: Erfolgreicher Login."""
        self._register_user()
        response = self.client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "passwort123"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["email"], "test@example.com")

    def test_login_wrong_password(self):
        """Test: Login mit falschem Passwort."""
        self._register_user()
        response = self.client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "falsch"},
        )
        self.assertEqual(response.status_code, 401)

    def test_login_user_not_found(self):
        """Test: Login mit nicht existierendem Benutzer."""
        response = self.client.post(
            "/api/auth/login",
            json={"email": "nicht@da.com", "password": "passwort123"},
        )
        self.assertEqual(response.status_code, 401)

    def test_me_endpoint(self):
        """Test: /me Endpoint mit gueltigem Token."""
        self._register_user()
        token = self._login_user()
        response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["user"]["username"], "testuser")

    def test_me_without_token(self):
        """Test: /me Endpoint ohne Token."""
        response = self.client.get("/api/auth/me")
        self.assertEqual(response.status_code, 401)

    # ==================== RECIPES TESTS ====================

    def test_create_and_list_recipes(self):
        """Test: Rezept erstellen und auflisten."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen
        response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 201)

        # Rezepte auflisten
        response = self.client.get("/api/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["recipes"]), 1)

    def test_get_recipe_by_id(self):
        """Test: Einzelnes Rezept abrufen."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen
        create_response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        recipe_id = create_response.get_json()["recipe"]["id"]

        # Rezept abrufen
        response = self.client.get(f"/api/recipes/{recipe_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["recipe"]["title"], "Test")

    def test_get_recipe_not_found(self):
        """Test: Nicht existierendes Rezept abrufen."""
        response = self.client.get("/api/recipes/999")
        self.assertEqual(response.status_code, 404)

    def test_create_recipe_validation(self):
        """Test: Rezept ohne Pflichtfelder erstellen."""
        self._register_user()
        token = self._login_user()

        response = self.client.post(
            "/api/recipes",
            json={"title": "Nur Titel"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_create_recipe_without_auth(self):
        """Test: Rezept ohne Authentifizierung erstellen."""
        response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_recipe(self):
        """Test: Eigene Rezept aktualisieren."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen
        create_response = self.client.post(
            "/api/recipes",
            json={"title": "Alt", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        recipe_id = create_response.get_json()["recipe"]["id"]

        # Rezept aktualisieren
        response = self.client.put(
            f"/api/recipes/{recipe_id}",
            json={"title": "Neu", "ingredients": "Neue Zutat", "steps": "Neuer Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["recipe"]["title"], "Neu")

    def test_update_recipe_not_owner(self):
        """Test: Fremdes Rezept aktualisieren (sollte fehlschlagen)."""
        # Erster Benutzer erstellt Rezept
        self._register_user("user1", "user1@example.com")
        token1 = self._login_user("user1@example.com")
        create_response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token1}"},
        )
        recipe_id = create_response.get_json()["recipe"]["id"]

        # Zweiter Benutzer versucht zu aktualisieren
        self._register_user("user2", "user2@example.com")
        token2 = self._login_user("user2@example.com")
        response = self.client.put(
            f"/api/recipes/{recipe_id}",
            json={"title": "Geaendert", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token2}"},
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_recipe(self):
        """Test: Eigenes Rezept loeschen."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen
        create_response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        recipe_id = create_response.get_json()["recipe"]["id"]

        # Rezept loeschen
        response = self.client.delete(
            f"/api/recipes/{recipe_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        # Pruefen ob geloescht
        response = self.client.get(f"/api/recipes/{recipe_id}")
        self.assertEqual(response.status_code, 404)

    # ==================== COMMENTS TESTS ====================

    def test_create_and_list_comments(self):
        """Test: Kommentar erstellen und auflisten."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen
        recipe_response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        recipe_id = recipe_response.get_json()["recipe"]["id"]

        # Kommentar erstellen
        response = self.client.post(
            f"/api/recipes/{recipe_id}/comments",
            json={"content": "Super Rezept!"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 201)

        # Kommentare auflisten
        response = self.client.get(f"/api/recipes/{recipe_id}/comments")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["comments"]), 1)

    def test_create_comment_on_nonexistent_recipe(self):
        """Test: Kommentar auf nicht existierendem Rezept."""
        self._register_user()
        token = self._login_user()

        response = self.client.post(
            "/api/recipes/999/comments",
            json={"content": "Test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 404)

    # ==================== FAVORITES TESTS ====================

    def test_add_and_list_favorites(self):
        """Test: Favorit hinzufuegen und auflisten."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen
        recipe_response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        recipe_id = recipe_response.get_json()["recipe"]["id"]

        # Zu Favoriten hinzufuegen
        response = self.client.post(
            f"/api/recipes/{recipe_id}/favorite",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 201)

        # Favoriten auflisten
        response = self.client.get(
            "/api/favorites",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["favorites"]), 1)

    def test_remove_favorite(self):
        """Test: Favorit entfernen."""
        self._register_user()
        token = self._login_user()

        # Rezept erstellen und favorisieren
        recipe_response = self.client.post(
            "/api/recipes",
            json={"title": "Test", "ingredients": "Zutat", "steps": "Schritt"},
            headers={"Authorization": f"Bearer {token}"},
        )
        recipe_id = recipe_response.get_json()["recipe"]["id"]
        self.client.post(
            f"/api/recipes/{recipe_id}/favorite",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Favorit entfernen
        response = self.client.delete(
            f"/api/recipes/{recipe_id}/favorite",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        # Pruefen ob entfernt
        response = self.client.get(
            "/api/favorites",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(len(response.get_json()["favorites"]), 0)

    def test_remove_nonexistent_favorite(self):
        """Test: Nicht existierenden Favorit entfernen."""
        self._register_user()
        token = self._login_user()

        response = self.client.delete(
            "/api/recipes/999/favorite",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
