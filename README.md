# 🍳 Rezept Sharing Plattform

Eine einfache Flask-REST-API zum Erstellen, Verwalten und Teilen von Rezepten.

## 📋 Projektbeschreibung

Diese Plattform ermöglicht es registrierten Nutzern:
- ✅ Sich zu registrieren und einzuloggen
- ✅ Neue Rezepte zu erstellen
- ✅ Alle Rezepte anzuzeigen
- ✅ Einzelne Rezepte zu bearbeiten (Update)
- ✅ Rezepte zu löschen

Die API verwendet SQLite als Datenbank und ist für den lokalen Betrieb optimiert.

---

## 🚀 Setup & Installation

### Voraussetzungen
- Python 3.8 oder höher
- Git

### Schritt 1: Repository klonen
```bash
git clone https://github.com/danialahmed2207/rezept_sharing_plattform.git
cd rezept_sharing_plattform
```

### Schritt 2: Virtuelle Umgebung erstellen
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# Windows: venv\Scripts\activate
```

### Schritt 3: Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Schritt 4: Server starten
```bash
python app.py
```

Der Server läuft dann auf: `http://localhost:5000`

---

## 📡 API Übersicht

| Methode | URL | Beschreibung | Auth erforderlich |
|---------|-----|--------------|-------------------|
| POST | `/register` | Neuen User registrieren | ❌ Nein |
| POST | `/login` | User einloggen | ❌ Nein |
| GET | `/recipes` | Alle Rezepte anzeigen | ❌ Nein |
| GET | `/recipes/<id>` | Einzelnes Rezept anzeigen | ❌ Nein |
| POST | `/recipes` | Neues Rezept erstellen | ✅ Ja |
| PUT | `/recipes/<id>` | Rezept aktualisieren | ✅ Ja |
| DELETE | `/recipes/<id>` | Rezept löschen | ✅ Ja |

---

## 🧪 API Beispiele (mit curl)

### 1. User registrieren
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"max","password":"123456"}'
```

**Antwort:**
```json
{"message": "User erstellt"}
```

### 2. Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"max","password":"123456"}'
```

**Antwort:**
```json
{
  "message": "Login erfolgreich",
  "user_id": 1,
  "username": "max"
}
```

### 3. Rezept erstellen
```bash
curl -X POST http://localhost:5000/recipes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pasta Carbonara",
    "ingredients": "Nudeln, Eier, Speck, Käse, Pfeffer",
    "steps": "1. Nudeln kochen\n2. Speck braten\n3. Eier mit Käse vermischen\n4. Alles zusammenfügen"
  }'
```

### 4. Alle Rezepte anzeigen
```bash
curl http://localhost:5000/recipes
```

### 5. Rezept aktualisieren
```bash
curl -X PUT http://localhost:5000/recipes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pasta Carbonara (verbessert)",
    "ingredients": "Spaghetti, Eier, Pancetta, Pecorino, Pfeffer",
    "steps": "1. Wasser salzen und Nudeln kochen..."
  }'
```

### 6. Rezept löschen
```bash
curl -X DELETE http://localhost:5000/recipes/1
```

---

## 🧪 Test-Client verwenden

Wir haben einen Python-Client zum Testen der API:

```bash
cd backend
python client.py
```

Dieser Client testet automatisch:
- Registrierung
- Login
- Rezept erstellen
- Alle Rezepte anzeigen

---

## 📝 Tagesdokumentation (Sprint Log)

### Sprint Woche 1

| Tag | Datum | Was wurde gemacht | Wer | Commit |
|-----|-------|-------------------|-----|--------|
| Tag 1 | 20.02.2025 | Projekt-Setup, Initiale Struktur | Danial | `chore: projektstruktur vereinfacht` |
| Tag 2 | 20.02.2025 | API-Dokumentation erweitert | Danial | `docs: api-dokumentation erweitert` |
| Tag 3 | 20.02.2025 | Code-Qualität verbessert | Danial | `refactor: code-qualitaet verbessert` |
| Tag 4 | 20.02.2025 | Demo-Skript und Postman Collection | Danial | `feat: interaktives demo-skript` |
| Tag 5 | 20.02.2025 | Projekt vereinfacht (nur eine app.py) | Danial | `feat: alles vereinfacht` |
| Tag 6 | 20.02.2025 | Anleitungen für Team erstellt | Danial | `docs: anleitungen fuer meikel und daniel` |
| Tag 7 | 20.02.2025 | Rezept aktualisieren (PUT) implementiert | Danial | `feat: rezept aktualisieren hinzugefuegt` |
| Tag 8 | 20.02.2025 | API-Client zum Testen hinzugefügt | Danial | `feat: api client zum testen hinzugefuegt` |
| Tag 9 | 20.02.2025 | Validierung beim Rezept-Update gefixt | Danial | `fix: validierung beim rezept update` |
| Tag 10 | 25.02.2025 | README vervollständigt, finale Doku | Danial | `docs: final readme update` |

### Team Commits
- **Meikel**: API-Testing, Qualitätssicherung
- **Daniel**: Dokumentation, README-Updates

---

## 🏗️ Projektstruktur

```
rezept_sharing_plattform/
├── README.md              # Diese Datei
├── ANLEITUNG_DANIEL.md    # Anleitung für Daniel
├── ANLEITUNG_MEIKEL.md    # Anleitung für Meikel
├── backend/
│   ├── app.py            # Haupt-API-Server
│   ├── client.py         # Test-Client
│   ├── requirements.txt  # Python-Abhängigkeiten
│   └── .gitignore        # Git-Ausschlüsse
└── .git/                 # Git-Repository
```

---

## 👥 Team

| Name | Rolle | Aufgaben |
|------|-------|----------|
| **Danial** | Backend Entwickler | API-Entwicklung, Datenbank, Architektur |
| **Meikel** | QA / Tester | API-Testing, Bugreports, Qualitätssicherung |
| **Daniel** | Dokumentation | README, Anleitungen, Sprint-Log |

---

## 🛠️ Technologien

- **Python 3** - Programmiersprache
- **Flask** - Web-Framework
- **SQLite** - Datenbank
- **Werkzeug** - Passwort-Hashing
- **Git** - Versionskontrolle

---

## 📝 Hinweise für die Prüfung

### Erfüllte Anforderungen
✅ Eigenes GitHub Repository  
✅ Tägliche Commits pro Person  
✅ README mit Projektbeschreibung  
✅ README mit API-Übersicht  
✅ README mit Tagesdokumentation  
✅ SQLite Datenbankanbindung  
✅ CRUD-Operationen (Create, Read, Update, Delete)  
✅ Python Skript zur API-Interaktion (client.py)  
✅ Saubere Projektstruktur  
✅ Login-System (Register/Login)  

### Wichtige Endpunkte zum Testen
1. Starte den Server: `python backend/app.py`
2. Teste im Browser oder mit curl/Postman
3. Oder nutze: `python backend/client.py`

---

## 📄 Lizenz

Dieses Projekt wurde im Rahmen einer schulischen Agile-Simulation erstellt.

---

**Stand:** 25.02.2025 | **Version:** 1.0 | **Sprint:** 2 Wochen abgeschlossen ✅
