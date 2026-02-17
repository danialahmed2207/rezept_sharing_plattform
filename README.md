# Rezept Sharing Plattform (Projektphase)

Dieses Projekt ist fuer eine 2-woechige Backend-Teamphase aufgebaut.
Es erfuellt die Pflichtpunkte:

- Datenbankanbindung (SQLite)
- CRUD-Operationen
- Login-System (JWT-Token)
- Python-Skript zur API-Interaktion
- Saubere Projektstruktur mit Frontend/Backend-Trennung

## Projektstruktur

```txt
rezept_sharing_plattform/
|- frontend/
|  |- index.html
|  |- script.js
|  |- style.css
|  |- requirements.txt
|- backend/
|  |- app/
|  |  |- __init__.py
|  |  |- db.py
|  |  |- security.py
|  |  |- routes_auth.py
|  |  |- routes_recipes.py
|  |  |- routes_comments.py
|  |  |- routes_favorites.py
|  |- scripts/
|  |  |- api_client.py
|  |- tests/
|  |  |- test_api.py
|  |- run.py
|  |- requirements.txt
|  |- .env.example
|- ANLEITUNG_WIE_WIR_VORGEHEN.md
|- PROJECT_CHECKLIST.md
|- README.md
|- .gitignore
```

## Team-Setup (einmalig)

1. Repository klonen:

```bash
git clone <URL>
cd rezept_sharing_plattform
```

2. Frontend-Umgebung einrichten:

```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Backend-Umgebung einrichten:

```bash
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

4. Lokale Umgebungsdatei anlegen:

```bash
cp .env.example .env
```

## Backend starten

```bash
cd backend
source venv/bin/activate
python3 run.py
```

Backend laeuft dann auf `http://127.0.0.1:5000`.

## Frontend starten (statisch)

```bash
cd frontend
python3 -m http.server 5500
```

Frontend: `http://127.0.0.1:5500`

## API-Uebersicht

### Authentifizierung

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me` (mit Token)

### Rezepte

- `GET /api/recipes`
- `GET /api/recipes/<id>`
- `POST /api/recipes` (mit Token)
- `PUT /api/recipes/<id>` (mit Token, nur Besitzer)
- `DELETE /api/recipes/<id>` (mit Token, nur Besitzer)

### Kommentare

- `GET /api/recipes/<id>/comments`
- `POST /api/recipes/<id>/comments` (mit Token)
- `PUT /api/comments/<id>` (mit Token, nur Besitzer)
- `DELETE /api/comments/<id>` (mit Token, nur Besitzer)

### Favoriten

- `POST /api/recipes/<id>/favorite` (mit Token)
- `DELETE /api/recipes/<id>/favorite` (mit Token)
- `GET /api/favorites` (mit Token)

## Python-Client-Skript

Das Skript fuehrt einen kompletten Demo-Ablauf aus:
Registrierung -> Anmeldung -> Rezept erstellen -> Kommentar -> Favorit.

```bash
cd backend
source venv/bin/activate
python3 scripts/api_client.py
```

## Tests ausfuehren

```bash
cd backend
source venv/bin/activate
python3 -m unittest discover -s tests -v
```

## Taegliche Dokumentation (Vorlage)

Tragt hier pro Teammitglied taeglich eure Arbeit ein.

| Datum | Teammitglied | Was wurde gemacht? | Commit-Link |
|---|---|---|---|
| YYYY-MM-DD | Name | Beispiel: Login-Endpunkt umgesetzt | URL |
| YYYY-MM-DD | Name | Beispiel: CRUD fuer Rezepte abgeschlossen | URL |

## Sprint-Plan (einfach)

### Sprint 1

- Datenmodell finalisieren
- Auth (Registrierung/Anmeldung)
- CRUD fuer Rezepte
- README-Grundstruktur

### Sprint 2

- Kommentare + Favoriten
- Python-API-Client
- Tests + Fehlerbehebung
- Demo + Abschlusspraesentation

## Git-Workflow (empfohlen)

- Taeglich mindestens 1 Commit pro Person
- Branch-Namen: `feature/...`, `fix/...`, `docs/...`, `test/...`
- Commit-Praefixe:
  - `feat:` fuer neue Funktionen
  - `fix:` fuer Fehlerbehebungen
  - `docs:` fuer Dokumentation
  - `test:` fuer Tests

## Wichtiger Hinweis fuer euer Team

Eine ausfuehrliche Schritt-fuer-Schritt-Anleitung fuer Einsteiger liegt in der separaten Datei:
`ANLEITUNG_WIE_WIR_VORGEHEN.md`
