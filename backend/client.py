"""
Einfacher Client zum Testen der API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_register():
    """Testet Registrierung"""
    print("\n=== Test: Registrierung ===")
    data = {
        "username": "testuser",
        "password": "123456"
    }
    r = requests.post(f"{BASE_URL}/register", json=data)
    print(f"Status: {r.status_code}")
    print(f"Antwort: {r.json()}")

def test_login():
    """Testet Login"""
    print("\n=== Test: Login ===")
    data = {
        "username": "testuser",
        "password": "123456"
    }
    r = requests.post(f"{BASE_URL}/login", json=data)
    print(f"Status: {r.status_code}")
    print(f"Antwort: {r.json()}")
    return r.json().get("user_id")

def test_create_recipe():
    """Testet Rezept erstellen"""
    print("\n=== Test: Rezept erstellen ===")
    data = {
        "title": "Pasta Carbonara",
        "ingredients": "Nudeln, Eier, Speck, Käse",
        "steps": "1. Nudeln kochen\n2. Speck braten\n3. Mischen"
    }
    r = requests.post(f"{BASE_URL}/recipes", json=data)
    print(f"Status: {r.status_code}")
    print(f"Antwort: {r.json()}")

def test_get_recipes():
    """Testet alle Rezepte anzeigen"""
    print("\n=== Test: Alle Rezepte ===")
    r = requests.get(f"{BASE_URL}/recipes")
    print(f"Status: {r.status_code}")
    print(f"Antwort: {json.dumps(r.json(), indent=2)}")

if __name__ == "__main__":
    print("API Client gestartet...")
    print("Stelle sicher, dass das Backend läuft!")
    print("Starte mit: python app.py")
    
    input("\nDrücke Enter zum Starten...")
    
    try:
        test_register()
        test_login()
        test_create_recipe()
        test_get_recipes()
        print("\n✅ Alle Tests fertig!")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        print("Ist das Backend gestartet?")
