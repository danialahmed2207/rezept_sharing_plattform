# 🎓 Präsentation: Rezept Sharing Plattform

**Dauer:** 8-10 Minuten  
**Zielgruppe:** Prüfer/Kursleiter  
**Format:** Live-Demo + Kurzvorstellung

---

## 📋 Vorbereitung vor der Präsi

### Technische Checkliste:
- [ ] Laptop vollgeladen
- [ ] Terminal geöffnet
- [ ] Projektordner bereit: `cd /Users/danialahmed/Projekt_Meikel_Daniel_Danial/rezept_sharing_plattform-aktuell/backend`
- [ ] Virtuelle Umgebung aktiviert: `source venv/bin/activate`
- [ ] Server kann gestartet werden: `python app.py`
- [ ] GitHub Repository offen im Browser (als Backup)
- [ ] README.md offen (zur Referenz)

---

## 🎬 Das Skript (Minute für Minute)

### **MINUTE 0-1: Einleitung & Projektübersicht**

**Du sagst:**
> "Guten Tag! Ich präsentiere heute unser Team-Projekt: Die **Rezept Sharing Plattform**.
>
> Wir sind ein Team aus drei Personen: Ich bin Danial und zuständig für das Backend, Meikel kümmert sich um Testing und Daniel um die Dokumentation.
>
> Das Projekt ist eine **REST-API** mit der man Rezepte erstellen, anzeigen, bearbeiten und löschen kann – also ein klassisches **CRUD-System** mit Benutzer-Login."

**Was du zeigst:**
- Kurz das Projekt-Verzeichnis im Terminal zeigen
- Oder: README.md im Browser öffnen

**Git-Befehl zum Zeigen:**
```bash
# Zeigt die letzten Commits
pwd
git log --oneline -10
```

---

### **MINUTE 1-2: Anforderungen & Technologien**

**Du sagst:**
> "Unser Projekt erfüllt alle gestellten Anforderungen:
> - ✅ Eigenes GitHub Repository mit täglichen Commits
> - ✅ SQLite Datenbank
> - ✅ Vollständige CRUD-Operationen
> - ✅ Login-System mit Registrierung
> - ✅ Python-Client zum Testen
> - ✅ Vollständige Dokumentation im README
>
> Technisch arbeiten wir mit **Python, Flask und SQLite**. Flask ist ein leichtgewichtiges Web-Framework, SQLite eine dateibasierte Datenbank – perfekt für dieses Projekt."

**Was du zeigst:**
```bash
# Zeigt die Projektstruktur
ls -la
cat backend/requirements.txt
```

---

### **MINUTE 2-5: LIVE-DEMO (Das Herzstück)**

**Du sagst:**
> "Ich zeige Ihnen jetzt die API in Aktion. Wir starten den Server und testen die wichtigsten Funktionen."

#### **Schritt 1: Server starten**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Sage:**
> "Der Server läuft jetzt auf Port 5000. Ich öffne ein zweites Terminal für die Tests."

#### **Schritt 2: Zweites Terminal öffnen**

```bash
# User registrieren
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","password":"123456"}'
```

**Erwartete Antwort:**
```json
{"message": "User erstellt"}
```

**Du sagst:**
> "Erfolgreich registriert. Das Passwort wird natürlich gehasht gespeichert."

#### **Schritt 3: Login**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","password":"123456"}'
```

**Erwartete Antwort:**
```json
{"message": "Login erfolgreich", "user_id": 1, "username": "demo_user"}
```

**Du sagst:**
> "Login funktioniert. Die API gibt die User-ID zurück, die wir für das Erstellen von Rezepten brauchen."

#### **Schritt 4: Rezept erstellen**

```bash
curl -X POST http://localhost:5000/recipes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pasta Carbonara",
    "ingredients": "Spaghetti, Eier, Speck, Käse, Pfeffer",
    "steps": "1. Nudeln kochen\n2. Speck braten\n3. Eier mit Käse vermischen\n4. Zusammenfügen"
  }'
```

**Erwartete Antwort:**
```json
{"message": "Rezept erstellt", "id": 1}
```

**Du sagst:**
> "Rezept erfolgreich erstellt mit ID 1."

#### **Schritt 5: Alle Rezepte anzeigen**

```bash
curl http://localhost:5000/recipes
```

**Du sagst:**
> "Hier sehen wir alle gespeicherten Rezepte mit Zeitstempel."

#### **Schritt 6: Rezept aktualisieren (UPDATE)**

```bash
curl -X PUT http://localhost:5000/recipes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pasta Carbonara Deluxe",
    "ingredients": "Spaghetti, Eier, Pancetta, Pecorino, schwarzer Pfeffer",
    "steps": "1. Salzwasser zum Kochen bringen..."
  }'
```

**Erwartete Antwort:**
```json
{"message": "Rezept aktualisiert"}
```

**Du sagst:**
> "Das Rezept wurde aktualisiert. Wir haben hier auch Validierung eingebaut – leere Felder werden abgelehnt."

#### **Schritt 7: Löschen (Optional, zeigen wenn Zeit ist)**

```bash
curl -X DELETE http://localhost:5000/recipes/1
```

---

### **MINUTE 5-6: Test-Client Demo**

**Du sagst:**
> "Neben den curl-Befehlen haben wir auch einen Python-Client geschrieben, der alle Tests automatisiert."

```bash
# Im dritten Terminal oder aktuelles curl abbrechen mit Ctrl+C
python client.py
```

**Was passiert:**
- Client zeigt nacheinander:
  - Registrierung
  - Login
  - Rezept erstellen
  - Alle Rezepte anzeigen

**Du sagst:**
> "Der Client testet automatisch alle wichtigen Funktionen und zeigt Status-Codes und Antworten an. Das erleichtert das Testing enorm."

---

### **MINUTE 6-8: Sprint-Dokumentation & Git**

**Du sagst:**
> "Ein wichtiger Teil des Projekts war die agile Arbeitsweise mit täglichen Commits."

**Zeige im Terminal:**
```bash
# Zeigt alle Branches
git branch -a

# Zeigt detaillierten Log
git log --oneline --graph --all | head -20
```

**Du sagst:**
> "Wir haben mit Feature-Branches gearbeitet:
> - `feat/tag2-update-rezept` für das Update-Feature
> - `feat/tag3-api-client` für den Test-Client
> - `fix/tag4-validierung` für Bugfixes
>
> Alles wurde über Pull Requests in den main Branch gemergt. Das sehen wir hier im Graphen."

**Zeige GitHub im Browser:**
- Öffne https://github.com/danialahmed2207/rezept_sharing_plattform
- Zeige kurz die Commit-History
- Zeige die README

---

### **MINUTE 8-9: Code-Qualität & Architektur**

**Du sagst:**
> "Schauen wir kurz in den Code. Die Architektur ist bewusst einfach gehalten."

**Zeige app.py (nur oberen Teil):**
```bash
head -60 backend/app.py
```

**Du sagst:**
> "Wir haben:
> - Klare Trennung der Routen
> - SQLite mit Row-Factory für Dictionary-Zugriff
> - Passwort-Hashing mit Werkzeug
> - Einfachen Login-Decorator
>
> Alles in einer Datei – übersichtlich und wartbar."

---

### **MINUTE 9-10: Fazit & Abschluss**

**Du sagst:**
> "Zusammenfassung:
> - Wir haben eine voll funktionsfähige REST-API gebaut
> - Alle CRUD-Operationen funktionieren
> - Login-System ist implementiert
> - Git-Workflow mit täglichen Commits
> - Vollständige Dokumentation
>
> Das Projekt ist technisch solide, gut dokumentiert und erfüllt alle Anforderungen."

**Frage:**
> "Gibt es Fragen?"

---

## 🆘 Notfall-Plan (Falls etwas schiefgeht)

### Server startet nicht:
```bash
# Port belegen?
lsof -ti:5000 | xargs kill -9
# Oder einfach neuen Port nutzen in app.py: port=5001
```

### Datenbank-Fehler:
```bash
# Datenbank löschen und neu erstellen
rm backend/database.db
cd backend && python app.py
```

### Curl funktioniert nicht:
> "Falls curl Probleme macht, zeige ich den Python-Client – der macht das Gleiche."

---

## 📊 Bewertungsmatrix (Zur eigenen Kontrolle)

| Kriterium | Gezeigt? | Notiz |
|-----------|----------|-------|
| Repository vorhanden | ⬜ | GitHub zeigen |
| Tägliche Commits | ⬜ | `git log` zeigen |
| README vollständig | ⬜ | Struktur erklären |
| API-Übersicht | ⬜ | Tabelle zeigen |
| Tagesdokumentation | ⬜ | Sprint-Log erwähnen |
| SQLite funktioniert | ⬜ | Rezepte erstellen/löschen |
| CRUD alle gezeigt | ⬜ | C-R-U-D durchgehen |
| Python Client gezeigt | ⬜ | `python client.py` |
| Login-System gezeigt | ⬜ | Register + Login |
| Präsentationszeit 8-10 Min | ⬜ | Zeit stoppen! |

---

## 💡 Tipps für die Präsi

1. **Rede langsam und deutlich** – Nervosität macht schnell
2. **Schau in die Kamera/zum Prüfer** – Nicht nur auf den Bildschirm
3. **Fehler sind ok** – Sag einfach: "Moment, ich prüfe das" und mach weiter
4. **Nicht zu tief in Code gehen** – Die Demo zählt, nicht jede Zeile Code
5. **Zeit im Blick behalten** – Wenn es schneller geht: Mehr Demo, weniger Rede

---

## 🎯 Zusammenfassung für dich

**Was du zeigen musst:**
1. ✅ Projektstruktur (1 Min)
2. ✅ Live-Demo der API (3 Min)
3. ✅ Git-History mit Commits (2 Min)
4. ✅ Test-Client (1 Min)
5. ✅ README-Doku (1 Min)

**Was du mitnehmen solltest:**
- Dieses Skript als Notiz
- Laptop vorbereitet
- Gute Laune 😊

---

**Viel Erfolg! Du schaffst das! 🚀**
