#!/usr/bin/env python3
"""
Demo API Client fuer die Rezept Sharing Plattform.

Dieses Skript testet alle wichtigen API-Endpunkte:
- Registrierung
- Login
- Rezept erstellen
- Rezepte auflisten
- Kommentar erstellen
- Favorit hinzufuegen
- Favoriten anzeigen

Verwendung:
    python scripts/api_client.py
    
    oder mit anderer URL:
    python scripts/api_client.py --base-url http://localhost:5000/api
"""

import argparse
import time

import requests


def show(label, response):
    """Zeigt API-Antwort formatiert an."""
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except ValueError:
        print(response.text)


def main():
    parser = argparse.ArgumentParser(description="Demo API Client fuer Rezept Sharing")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:5000/api",
        help="API Basis-URL (default: http://127.0.0.1:5000/api)",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    
    # Eindeutige Testdaten erstellen
    unique = int(time.time())
    username = f"testuser_{unique}"
    email = f"testuser_{unique}@example.com"
    password = "passwort123"

    print("\n" + "="*50)
    print("  REZEPT SHARING API - DEMO")
    print("="*50)
    print(f"\nAPI URL: {base_url}")
    print(f"Test-User: {username}")

    # 1. Registrierung
    register_payload = {
        "username": username,
        "email": email,
        "password": password,
    }
    register_resp = requests.post(
        f"{base_url}/auth/register", 
        json=register_payload, 
        timeout=10
    )
    show("1. REGISTRIERUNG", register_resp)

    if register_resp.status_code != 201:
        print("\n❌ Registrierung fehlgeschlagen!")
        return

    # 2. Login
    login_resp = requests.post(
        f"{base_url}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    show("2. LOGIN", login_resp)

    if login_resp.status_code != 200:
        print("\n❌ Login fehlgeschlagen!")
        return

    token = login_resp.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"\n✅ Token erhalten: {token[:20]}...")

    # 3. Rezept erstellen
    recipe_payload = {
        "title": "Schnelles Omelett",
        "ingredients": "2 Eier, Salz, Pfeffer, Butter",
        "steps": "1. Eier verquirlen\n2. Butter in Pfanne schmelzen\n3. Eier hineingeben\n4. Kurz stocken lassen",
    }
    recipe_resp = requests.post(
        f"{base_url}/recipes",
        json=recipe_payload,
        headers=headers,
        timeout=10,
    )
    show("3. REZEPT ERSTELLEN", recipe_resp)

    if recipe_resp.status_code != 201:
        print("\n❌ Rezept erstellen fehlgeschlagen!")
        return

    recipe_id = recipe_resp.json()["recipe"]["id"]
    print(f"\n✅ Rezept ID: {recipe_id}")

    # 4. Rezepte auflisten
    list_resp = requests.get(f"{base_url}/recipes", timeout=10)
    show("4. REZEPTE LISTEN", list_resp)

    # 5. Kommentar erstellen
    comment_resp = requests.post(
        f"{base_url}/recipes/{recipe_id}/comments",
        json={"content": "Schnell und lecker! 👍"},
        headers=headers,
        timeout=10,
    )
    show("5. KOMMENTAR ERSTELLEN", comment_resp)

    # 6. Favorit hinzufuegen
    favorite_resp = requests.post(
        f"{base_url}/recipes/{recipe_id}/favorite",
        headers=headers,
        timeout=10,
    )
    show("6. FAVORIT HINZUFUEGEN", favorite_resp)

    # 7. Favoriten anzeigen
    favorites_resp = requests.get(f"{base_url}/favorites", headers=headers, timeout=10)
    show("7. FAVORITEN ANZEIGEN", favorites_resp)

    # Zusammenfassung
    print("\n" + "="*50)
    print("  ZUSAMMENFASSUNG")
    print("="*50)
    tests = [
        ("Registrierung", register_resp.status_code == 201),
        ("Login", login_resp.status_code == 200),
        ("Rezept erstellen", recipe_resp.status_code == 201),
        ("Rezepte listen", list_resp.status_code == 200),
        ("Kommentar erstellen", comment_resp.status_code == 201),
        ("Favorit hinzufuegen", favorite_resp.status_code == 201),
        ("Favoriten anzeigen", favorites_resp.status_code == 200),
    ]
    
    for name, success in tests:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    passed = sum(1 for _, s in tests if s)
    print(f"\nErgebnis: {passed}/{len(tests)} Tests bestanden")
    
    if passed == len(tests):
        print("\n🎉 Alle API-Endpunkte funktionieren!")
    else:
        print("\n⚠️  Einige Tests sind fehlgeschlagen.")


if __name__ == "__main__":
    main()
