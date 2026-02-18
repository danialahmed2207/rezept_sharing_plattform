# Rezept Sharing Plattform

Eine einfache Backend-API fuer eine Rezept-Sharing-Plattform.
Erstellt im Rahmen einer zweiwöchigen Agile-Simulation.

## Technologien

- **Backend:** Flask (Python)
- **Datenbank:** SQLite
- **Authentifizierung:** JWT-Token

## Projektstruktur

```
rezept_sharing_plattform/
├── backend/
│   ├── app/                    # Flask Anwendung
│   │   ├── __init__.py         # App-Factory
│   │   ├── db.py               # Datenbank
│   │   ├── security.py         # JWT & Passwort-Hashing
│   │   ├── routes_auth.py      # Login/Register
│   │   ├── routes_recipes.py   # Rezepte CRUD
│   │   ├── routes_comments.py  # Kommentare
│   │   └── routes_favorites.py # Favoriten
│   ├── scripts/
│   │   └── api_client.py       # Python Demo-Skript
│   ├── tests/
│   │   └── test_api.py         # API Tests
│   ├── .env.example            # Umgebungsvariablen Vorlage
│   ├── .gitignore              # Git Ignore
│   ├── requirements.txt        # Python Abhängigkeiten
│   └── run.py                  # Start-Skript
└── README.md                   # Diese Datei
```

## Einrichtung

### 1. Repository klonen

```bash
git clone <URL>
cd rezept_sharing_plattform/backend
```

### 2. Virtuelle Umgebung erstellen

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate  # Windows
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen einrichten

```bash
cp .env.example .env
```

## Backend starten

```bash
python run.py
```

Die API läuft auf: `http://127.0.0.1:5000`

Health-Check: `GET http://127.0.0.1:5000/api/health`

## API Übersicht

### Authentifizierung

| Methode | Endpoint | Beschreibung | Auth |
|---------|----------|--------------|------|
| POST | `/api/auth/register` | Benutzer registrieren | Nein |
| POST | `/api/auth/login` | Benutzer anmelden | Nein |
| GET | `/api/auth/me` | Aktueller Benutzer | Ja |

### Rezepte

| Methode | Endpoint | Beschreibung | Auth |
|---------|----------|--------------|------|
| GET | `/api/recipes` | Alle Rezepte anzeigen | Nein |
| GET | `/api/recipes/<id>` | Einzelnes Rezept anzeigen | Nein |
| POST | `/api/recipes` | Rezept erstellen | Ja |
| PUT | `/api/recipes/<id>` | Rezept aktualisieren | Ja (Owner) |
| DELETE | `/api/recipes/<id>` | Rezept löschen | Ja (Owner) |

### Kommentare

| Methode | Endpoint | Beschreibung | Auth |
|---------|----------|--------------|------|
| GET | `/api/recipes/<id>/comments` | Kommentare zu Rezept | Nein |
| POST | `/api/recipes/<id>/comments` | Kommentar erstellen | Ja |
| PUT | `/api/comments/<id>` | Kommentar bearbeiten | Ja (Owner) |
| DELETE | `/api/comments/<id>` | Kommentar löschen | Ja (Owner) |

### Favoriten

| Methode | Endpoint | Beschreibung | Auth |
|---------|----------|--------------|------|
| GET | `/api/favorites` | Eigene Favoriten | Ja |
| POST | `/api/recipes/<id>/favorite` | Zu Favoriten hinzufügen | Ja |
| DELETE | `/api/recipes/<id>/favorite` | Aus Favoriten entfernen | Ja |

## API Beispiele

### 1. Health Check

```bash
curl http://127.0.0.1:5000/api/health
```

**Antwort:**
```json
{
  "status": "ok"
}
```

### 2. Registrierung

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "max",
    "email": "max@example.com",
    "password": "passwort123"
  }'
```

**Antwort (201 Created):**
```json
{
  "message": "Registrierung erfolgreich",
  "user": {
    "id": 1,
    "username": "max",
    "email": "max@example.com"
  }
}
```

**Fehler (400 Bad Request):**
```json
{
  "error": "Benutzername, E-Mail und Passwort sind Pflicht"
}
```

**Fehler (409 Conflict):**
```json
{
  "error": "Benutzername oder E-Mail existiert bereits"
}
```

### 3. Login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "max@example.com",
    "password": "passwort123"
  }'
```

**Antwort (200 OK):**
```json
{
  "message": "Login erfolgreich",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "max",
    "email": "max@example.com"
  }
}
```

**Fehler (401 Unauthorized):**
```json
{
  "error": "Login fehlgeschlagen"
}
```

### 4. Aktuellen Benutzer abfragen

```bash
curl http://127.0.0.1:5000/api/auth/me \
  -H "Authorization: Bearer <DEIN_TOKEN>"
```

**Antwort:**
```json
{
  "user": {
    "id": 1,
    "username": "max",
    "email": "max@example.com"
  }
}
```

### 5. Rezept erstellen

```bash
curl -X POST http://127.0.0.1:5000/api/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DEIN_TOKEN>" \
  -d '{
    "title": "Spaghetti Carbonara",
    "ingredients": "200g Spaghetti, 100g Speck, 2 Eier, 50g Parmesan, Pfeffer",
    "steps": "1. Spaghetti kochen\n2. Speck anbraten\n3. Eier mit Parmesan vermischen\n4. Alles verbinden"
  }'
```

**Antwort (201 Created):**
```json
{
  "message": "Rezept erstellt",
  "recipe": {
    "id": 1,
    "title": "Spaghetti Carbonara",
    "ingredients": "200g Spaghetti, 100g Speck, 2 Eier, 50g Parmesan, Pfeffer",
    "steps": "1. Spaghetti kochen\n2. Speck anbraten\n3. Eier mit Parmesan vermischen\n4. Alles verbinden",
    "owner_id": 1,
    "owner_username": "max",
    "comment_count": 0,
    "favorite_count": 0,
    "created_at": "2025-02-18T10:00:00",
    "updated_at": "2025-02-18T10:00:00"
  }
}
```

### 6. Alle Rezepte anzeigen

```bash
curl http://127.0.0.1:5000/api/recipes
```

**Antwort:**
```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Spaghetti Carbonara",
      "ingredients": "200g Spaghetti, 100g Speck...",
      "steps": "1. Spaghetti kochen...",
      "owner_id": 1,
      "owner_username": "max",
      "comment_count": 0,
      "favorite_count": 0,
      "created_at": "2025-02-18T10:00:00",
      "updated_at": "2025-02-18T10:00:00"
    }
  ]
}
```

### 7. Einzelnes Rezept anzeigen

```bash
curl http://127.0.0.1:5000/api/recipes/1
```

**Antwort:**
```json
{
  "recipe": {
    "id": 1,
    "title": "Spaghetti Carbonara",
    ...
  }
}
```

**Fehler (404 Not Found):**
```json
{
  "error": "Rezept nicht gefunden"
}
```

### 8. Rezept aktualisieren

```bash
curl -X PUT http://127.0.0.1:5000/api/recipes/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DEIN_TOKEN>" \
  -d '{
    "title": "Spaghetti Carbonara (verbessert)",
    "ingredients": "200g Spaghetti, 100g Pancetta, 2 Eier, 50g Pecorino, Pfeffer",
    "steps": "1. Spaghetti al dente kochen\n2. Pancetta knusprig braten\n3. Eier mit Käse vermischen\n4. Mit Nudelwasser cremig rühren"
  }'
```

**Antwort:**
```json
{
  "message": "Rezept aktualisiert",
  "recipe": {
    "id": 1,
    "title": "Spaghetti Carbonara (verbessert)",
    ...
  }
}
```

**Fehler (403 Forbidden):**
```json
{
  "error": "Nur der Owner darf aendern"
}
```

### 9. Rezept löschen

```bash
curl -X DELETE http://127.0.0.1:5000/api/recipes/1 \
  -H "Authorization: Bearer <DEIN_TOKEN>"
```

**Antwort:**
```json
{
  "message": "Rezept geloescht"
}
```

### 10. Kommentar erstellen

```bash
curl -X POST http://127.0.0.1:5000/api/recipes/1/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DEIN_TOKEN>" \
  -d '{
    "content": "Sehr lecker! Kann ich nur empfehlen."
  }'
```

**Antwort (201 Created):**
```json
{
  "message": "Kommentar erstellt",
  "comment": {
    "id": 1,
    "content": "Sehr lecker! Kann ich nur empfehlen.",
    "user_id": 1,
    "recipe_id": 1,
    "created_at": "2025-02-18T10:30:00"
  }
}
```

### 11. Kommentare anzeigen

```bash
curl http://127.0.0.1:5000/api/recipes/1/comments
```

**Antwort:**
```json
{
  "comments": [
    {
      "id": 1,
      "content": "Sehr lecker! Kann ich nur empfehlen.",
      "username": "max",
      "created_at": "2025-02-18T10:30:00"
    }
  ]
}
```

### 12. Zu Favoriten hinzufügen

```bash
curl -X POST http://127.0.0.1:5000/api/recipes/1/favorite \
  -H "Authorization: Bearer <DEIN_TOKEN>"
```

**Antwort:**
```json
{
  "message": "Zu Favoriten hinzugefuegt"
}
```

### 13. Favoriten anzeigen

```bash
curl http://127.0.0.1:5000/api/favorites \
  -H "Authorization: Bearer <DEIN_TOKEN>"
```

**Antwort:**
```json
{
  "favorites": [
    {
      "recipe_id": 1,
      "title": "Spaghetti Carbonara",
      "owner_username": "max"
    }
  ]
}
```

## Fehler-Codes

| Code | Bedeutung | Wann tritt es auf? |
|------|-----------|-------------------|
| 200 | OK | Anfrage erfolgreich |
| 201 | Created | Ressource erstellt |
| 400 | Bad Request | Fehlende/ungültige Daten |
| 401 | Unauthorized | Nicht eingeloggt |
| 403 | Forbidden | Keine Berechtigung |
| 404 | Not Found | Ressource nicht gefunden |
| 409 | Conflict | Ressource existiert bereits |

## Python API Client

Das Demo-Skript zeigt alle API-Funktionen:

```bash
cd backend
python scripts/api_client.py
```

## Tests ausführen

```bash
cd backend
python -m unittest discover -s tests -v
```

## Tägliche Dokumentation

| Datum | Teammitglied | Was wurde gemacht? | Commit |
|-------|--------------|-------------------|--------|
| 2025-02-18 | Name | Projekt-Setup bereinigt | `chore: projektstruktur vereinfacht` |
| 2025-02-18 | Name | API-Client verbessert | `test: api-client verbessert` |
| 2025-02-18 | Name | API-Doku erweitert | `docs: api-beispiele hinzugefuegt` |

## Git Workflow

```bash
# 1. Aktuellen Stand holen
git checkout main
git pull origin main

# 2. Neuen Branch erstellen
git checkout -b feature/beschreibung

# 3. Änderungen machen...

# 4. Committen
git add .
git commit -m "feat: beschreibung"

# 5. Hochladen
git push -u origin feature/beschreibung
```

## Commit Message Konventionen

- `feat:` - Neue Funktion
- `fix:` - Fehlerbehebung
- `docs:` - Dokumentation
- `test:` - Tests
- `chore:` - Wartung/Setup

## Sprint Ziele

- [x] Projekt-Setup
- [x] API vollständig testen
- [x] README mit API-Beispielen
- [ ] Demo vorbereiten
