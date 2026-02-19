#!/usr/bin/env python3
"""
Interaktives Demo-Skript fuer die Rezept Sharing Plattform.

Dieses Skript fuehrt Schritt fuer Schritt durch die API:
1. Health Check
2. Registrierung
3. Login
4. Rezept erstellen
5. Rezepte anzeigen
6. Kommentar erstellen
7. Zu Favoriten hinzufuegen
8. Favoriten anzeigen

Verwendung:
    python scripts/demo.py

oder mit anderer URL:
    python scripts/demo.py --url http://localhost:5000/api
"""

import argparse
import time

import requests


def print_header(text):
    """Gibt einen formatierten Header aus."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_response(label, response):
    """Gibt eine API-Antwort formatiert aus."""
    print(f"\n📡 {label}")
    print(f"   Status: {response.status_code}")
    try:
        import json
        data = response.json()
        print(f"   Antwort: {json.dumps(data, indent=6, ensure_ascii=False)}")
    except ValueError:
        print(f"   Antwort: {response.text}")


def wait_for_user():
    """Wartet auf Enter-Taste."""
    input("\n➡️  Enter druecken zum Fortfahren...")


def main():
    parser = argparse.ArgumentParser(
        description="Interaktives Demo fuer Rezept Sharing API"
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:5000/api",
        help="API Basis-URL (default: http://127.0.0.1:5000/api)",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatischer Modus (ohne Warten auf Enter)",
    )
    args = parser.parse_args()

    base_url = args.url.rstrip("/")
    auto_mode = args.auto

    print("\n" + "=" * 60)
    print("  🍳 REZEPT SHARING PLATTFORM - DEMO")
    print("=" * 60)
    print(f"\nAPI URL: {base_url}")
    print("\nDieses Demo fuehrt dich durch alle wichtigen API-Funktionen.")
    print("Stelle sicher, dass das Backend laeuft:")
    print("  python backend/run.py")

    if not auto_mode:
        input("\n➡️  Enter druecken zum Starten...")

    # Eindeutige Testdaten
    unique = int(time.time())
    username = f"demo_user_{unique}"
    email = f"demo_{unique}@example.com"
    password = "demo123"
    token = None

    # ============================================
    # 1. Health Check
    # ============================================
    print_header("1. HEALTH CHECK")
    print("Prueft ob die API erreichbar ist...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print_response("Health Check", response)
        if response.status_code == 200:
            print("\n✅ API ist erreichbar!")
        else:
            print("\n❌ API nicht erreichbar!")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Fehler: API nicht erreichbar!")
        print("   Bitte starte das Backend:")
        print("   python backend/run.py")
        return

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 2. Registrierung
    # ============================================
    print_header("2. REGISTRIERUNG")
    print(f"Erstellt einen neuen Benutzer:")
    print(f"  Benutzername: {username}")
    print(f"  E-Mail: {email}")
    print(f"  Passwort: {password}")

    register_data = {
        "username": username,
        "email": email,
        "password": password,
    }
    response = requests.post(
        f"{base_url}/auth/register",
        json=register_data,
        timeout=10,
    )
    print_response("Registrierung", response)

    if response.status_code != 201:
        print("\n❌ Registrierung fehlgeschlagen!")
        return
    print("\n✅ Benutzer erfolgreich registriert!")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 3. Login
    # ============================================
    print_header("3. LOGIN")
    print("Meldet den Benutzer an...")

    login_data = {
        "email": email,
        "password": password,
    }
    response = requests.post(
        f"{base_url}/auth/login",
        json=login_data,
        timeout=10,
    )
    print_response("Login", response)

    if response.status_code != 200:
        print("\n❌ Login fehlgeschlagen!")
        return

    token = response.json().get("token")
    print(f"\n✅ Login erfolgreich!")
    print(f"   Token: {token[:30]}...")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 4. Rezept erstellen
    # ============================================
    print_header("4. REZEPT ERSTELLEN")
    print("Erstellt ein neues Rezept...")

    recipe_data = {
        "title": "🍝 Spaghetti Carbonara",
        "ingredients": "400g Spaghetti, 200g Pancetta, 4 Eier, 100g Pecorino, Pfeffer, Salz",
        "steps": "1. Spaghetti al dente kochen\n"
                 "2. Pancetta knusprig braten\n"
                 "3. Eier mit geriebenem Kaese vermischen\n"
                 "4. Nudeln mit Pancetta vermischen\n"
                 "5. Ei-Kaese-Mischung hinzufuegen\n"
                 "6. Mit Nudelwasser cremig ruehren\n"
                 "7. Mit Pfeffer servieren",
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{base_url}/recipes",
        json=recipe_data,
        headers=headers,
        timeout=10,
    )
    print_response("Rezept erstellen", response)

    if response.status_code != 201:
        print("\n❌ Rezept erstellen fehlgeschlagen!")
        return

    recipe_id = response.json()["recipe"]["id"]
    print(f"\n✅ Rezept erstellt mit ID: {recipe_id}")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 5. Rezepte anzeigen
    # ============================================
    print_header("5. REZEPTE ANZEIGEN")
    print("Listet alle Rezepte auf...")

    response = requests.get(f"{base_url}/recipes", timeout=10)
    print_response("Rezepte auflisten", response)

    if response.status_code == 200:
        recipes = response.json().get("recipes", [])
        print(f"\n✅ {len(recipes)} Rezept(e) gefunden")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 6. Kommentar erstellen
    # ============================================
    print_header("6. KOMMENTAR ERSTELLEN")
    print(f"Fuegt einen Kommentar zu Rezept {recipe_id} hinzu...")

    comment_data = {"content": "Ein Klassiker! Einfach und lecker. 👨‍🍳"}
    response = requests.post(
        f"{base_url}/recipes/{recipe_id}/comments",
        json=comment_data,
        headers=headers,
        timeout=10,
    )
    print_response("Kommentar erstellen", response)

    if response.status_code == 201:
        print("\n✅ Kommentar erstellt!")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 7. Zu Favoriten hinzufuegen
    # ============================================
    print_header("7. ZU FAVORITEN HINZUFUEGEN")
    print(f"Fuegt Rezept {recipe_id} zu Favoriten hinzu...")

    response = requests.post(
        f"{base_url}/recipes/{recipe_id}/favorite",
        headers=headers,
        timeout=10,
    )
    print_response("Favorit hinzufuegen", response)

    if response.status_code == 201:
        print("\n✅ Zu Favoriten hinzugefuegt!")
    elif response.status_code == 200:
        print("\nℹ️  War bereits Favorit")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 8. Favoriten anzeigen
    # ============================================
    print_header("8. FAVORITEN ANZEIGEN")
    print("Listet alle Favoriten des Benutzers auf...")

    response = requests.get(
        f"{base_url}/favorites",
        headers=headers,
        timeout=10,
    )
    print_response("Favoriten anzeigen", response)

    if response.status_code == 200:
        favorites = response.json().get("favorites", [])
        print(f"\n✅ {len(favorites)} Favorit(en) gefunden")

    if not auto_mode:
        wait_for_user()

    # ============================================
    # 9. Zusammenfassung
    # ============================================
    print_header("9. ZUSAMMENFASSUNG")
    print("\n✅ Demo erfolgreich abgeschlossen!")
    print("\nDurchgefuehrte Aktionen:")
    print("  1. ✅ Health Check")
    print("  2. ✅ Registrierung")
    print("  3. ✅ Login")
    print("  4. ✅ Rezept erstellen")
    print("  5. ✅ Rezepte anzeigen")
    print("  6. ✅ Kommentar erstellen")
    print("  7. ✅ Zu Favoriten hinzufuegen")
    print("  8. ✅ Favoriten anzeigen")
    print("\nTest-Benutzer:")
    print(f"  Benutzername: {username}")
    print(f"  E-Mail: {email}")
    print(f"  Passwort: {password}")
    print("\n🎉 Viel Erfolg bei der Pruefung!")
    print("=" * 60)


if __name__ == "__main__":
    main()
