import argparse
import time

import requests


def show(label, response):
    print(f"\n== {label} ==")
    print(f"Status: {response.status_code}")
    try:
        print(response.json())
    except ValueError:
        print(response.text)


def main():
    parser = argparse.ArgumentParser(description="Demo API Client fuer Rezept Sharing")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:5000/api",
        help="API Basis-URL",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    unique = int(time.time())

    username = f"teammitglied_{unique}"
    email = f"teammitglied_{unique}@example.com"
    password = "passwort123"

    register_payload = {
        "username": username,
        "email": email,
        "password": password,
    }
    register_resp = requests.post(f"{base_url}/auth/register", json=register_payload, timeout=10)
    show("Registrierung", register_resp)

    login_resp = requests.post(
        f"{base_url}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    show("Anmeldung", login_resp)

    if login_resp.status_code != 200:
        print("\nLogin fehlgeschlagen, Demo wird beendet.")
        return

    token = login_resp.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}

    recipe_payload = {
        "title": "Schnelles Omelett",
        "ingredients": "2 Eier, Salz, Pfeffer, Butter",
        "steps": "Eier verquirlen, in Pfanne geben, kurz stocken lassen.",
    }
    recipe_resp = requests.post(
        f"{base_url}/recipes",
        json=recipe_payload,
        headers=headers,
        timeout=10,
    )
    show("Rezept erstellen", recipe_resp)

    if recipe_resp.status_code != 201:
        print("\nRezept konnte nicht erstellt werden, Demo wird beendet.")
        return

    recipe_id = recipe_resp.json()["recipe"]["id"]

    list_resp = requests.get(f"{base_url}/recipes", timeout=10)
    show("Rezepte anzeigen", list_resp)

    comment_resp = requests.post(
        f"{base_url}/recipes/{recipe_id}/comments",
        json={"content": "Schnell und lecker!"},
        headers=headers,
        timeout=10,
    )
    show("Kommentar erstellen", comment_resp)

    favorite_resp = requests.post(
        f"{base_url}/recipes/{recipe_id}/favorite",
        headers=headers,
        timeout=10,
    )
    show("Favorit hinzufuegen", favorite_resp)

    favorites_resp = requests.get(f"{base_url}/favorites", headers=headers, timeout=10)
    show("Favoriten anzeigen", favorites_resp)


if __name__ == "__main__":
    main()
