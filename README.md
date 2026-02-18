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

### Registrierung

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"max","email":"max@example.com","password":"passwort123"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"max@example.com","password":"passwort123"}'
```

### Rezept erstellen (mit Token)

```bash
curl -X POST http://127.0.0.1:5000/api/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <DEIN_TOKEN>" \
  -d '{"title":"Pasta","ingredients":"Nudeln, Sauce","steps":"Kochen, mischen"}'
```

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
- [ ] API vollständig testen
- [ ] README vervollständigen
- [ ] Demo vorbereiten
