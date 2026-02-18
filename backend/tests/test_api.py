"""
API Tests fuer die Rezept Sharing Plattform.

Diese Tests pruefen:
- Health Check
- Benutzer-Registrierung
- Login
- Rezept erstellen
- Rezepte auflisten

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

    def test_health_check(self):
        """Test: Health-Check Endpoint."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")

    def test_register_and_login(self):
        """Test: Registrierung und Login."""
        # Registrierung
        register_response = self.client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "passwort123",
            },
        )
        self.assertEqual(register_response.status_code, 201)
        data = register_response.get_json()
        self.assertEqual(data["user"]["username"], "testuser")
        self.assertEqual(data["user"]["email"], "test@example.com")

        # Login
        login_response = self.client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "passwort123",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        data = login_response.get_json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["email"], "test@example.com")

    def test_create_and_list_recipes(self):
        """Test: Rezept erstellen und auflisten."""
        # Erst Benutzer erstellen und einloggen
        self.client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "passwort123",
            },
        )
        login_response = self.client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "passwort123",
            },
        )
        token = login_response.get_json()["token"]

        # Rezept erstellen
        create_response = self.client.post(
            "/api/recipes",
            json={
                "title": "Test Rezept",
                "ingredients": "Zutat 1, Zutat 2",
                "steps": "Schritt 1, Schritt 2",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(create_response.status_code, 201)
        data = create_response.get_json()
        self.assertEqual(data["recipe"]["title"], "Test Rezept")

        # Rezepte auflisten
        list_response = self.client.get("/api/recipes")
        self.assertEqual(list_response.status_code, 200)
        data = list_response.get_json()
        self.assertEqual(len(data["recipes"]), 1)
        self.assertEqual(data["recipes"][0]["title"], "Test Rezept")

    def test_register_validation(self):
        """Test: Validierung bei Registrierung."""
        # Fehlende Daten
        response = self.client.post(
            "/api/auth/register",
            json={"username": "test"},  # Email und Passwort fehlen
        )
        self.assertEqual(response.status_code, 400)

        # Zu kurzes Passwort
        response = self.client.post(
            "/api/auth/register",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "123",  # Zu kurz
            },
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
