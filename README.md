# Rezept Sharing Plattform

Einfache Flask-API für Rezepte.

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## API Endpunkte

| Methode | URL | Beschreibung |
|---------|-----|--------------|
| POST | /register | User registrieren |
| POST | /login | Einloggen |
| GET | /recipes | Alle Rezepte |
| POST | /recipes | Rezept erstellen |
| GET | /recipes/<id> | Ein Rezept |
| DELETE | /recipes/<id> | Rezept löschen |

## Beispiele

### Registrieren
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"max","password":"123456"}'
```

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"max","password":"123456"}'
```

### Rezept erstellen
```bash
curl -X POST http://localhost:5000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"Pasta","ingredients":"Nudeln","steps":"Kochen"}'
```

## Team

- Danial - API erstellt
- Meikel - Tests gemacht
- Daniel -
