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
    def setUp(self):
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
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_register_login_and_create_recipe(self):
        register_response = self.client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "passwort123",
            },
        )
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "passwort123",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.get_json()["token"]

        create_recipe_response = self.client.post(
            "/api/recipes",
            json={
                "title": "Pasta",
                "ingredients": "Nudeln, Wasser, Salz",
                "steps": "Kochen und servieren",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(create_recipe_response.status_code, 201)

        list_response = self.client.get("/api/recipes")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.get_json()["recipes"]), 1)


if __name__ == "__main__":
    unittest.main()
