# Anleitung: Wie wir als Team vorgehen

Diese Datei ist fuer Einsteiger. Bitte genau in der Reihenfolge arbeiten.

## 1. Einmalige Einrichtung pro Teammitglied

1. Repository klonen:

```bash
git clone <URL>
cd rezept_sharing_plattform
```

2. Backend einrichten:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
```

3. Frontend einrichten:

```bash
cd ../frontend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## 2. Taeglicher Start (jeden Tag)

1. In den Projektordner wechseln:

```bash
cd rezept_sharing_plattform
```

2. Neueste Aenderungen holen:

```bash
git checkout main
git pull origin main
```

3. Eigenen Arbeits-Branch erstellen:

```bash
git checkout -b feature/<kurze-beschreibung>
```

Beispiel:

```bash
git checkout -b feature/rezept-formular
```

## 3. Lokales Entwickeln und Testen

1. Backend starten:

```bash
cd backend
source venv/bin/activate
python3 run.py
```

2. Frontend in zweitem Terminal starten:

```bash
cd frontend
python3 -m http.server 5500
```

3. Tests ausfuehren (Backend):

```bash
cd backend
source venv/bin/activate
python3 -m unittest discover -s tests -v
```

## 4. Commit Schritt fuer Schritt (wichtig)

1. Geaenderte Dateien anschauen:

```bash
git status
```

2. Inhalte vor dem Commit pruefen:

```bash
git diff
```

3. Gewuenschte Dateien zum Commit hinzufuegen:

```bash
git add <datei1> <datei2>
```

Oder alles hinzufuegen:

```bash
git add .
```

4. Commit erstellen:

```bash
git commit -m "feat: rezeptformular verbessert"
```

5. Branch auf GitHub hochladen:

```bash
git push -u origin feature/<kurze-beschreibung>
```

6. Auf GitHub Pull Request auf `main` erstellen und im Team kurz pruefen.

## 5. Regeln fuer Commit-Nachrichten

- `feat:` neue Funktion
- `fix:` Fehlerbehebung
- `docs:` Dokumentation
- `test:` Tests
- `refactor:` Struktur verbessert, Verhalten gleich

Gute Beispiele:

- `feat: rezept erstellen endpoint hinzugefuegt`
- `fix: login fehler bei leerer email behoben`
- `docs: anleitung fuer setup ergaenzt`

## 6. 10-Tage-Plan mit echten Commit-Ideen

Hinweis: Nur echte Arbeit committen. Keine kuenstlichen oder leeren Commits.

Tag 1:
- Aufgabe: Projekt lokal starten und Team-Rollen festlegen
- Beispiel-Commit: `docs: lokale einrichtung und teamrollen dokumentiert`

Tag 2:
- Aufgabe: Registrierung und Anmeldung pruefen
- Beispiel-Commit: `test: auth ablaeufe manuell getestet und notizen ergaenzt`

Tag 3:
- Aufgabe: Rezepte erstellen/listen verbessern
- Beispiel-Commit: `feat: validierung fuer rezeptdaten verbessert`

Tag 4:
- Aufgabe: Kommentare pruefen und Fehler beheben
- Beispiel-Commit: `fix: kommentare endpoint validierung korrigiert`

Tag 5:
- Aufgabe: Favoriten-Funktion testen
- Beispiel-Commit: `test: favoriten ablaeufe ergaenzt`

Tag 6:
- Aufgabe: Frontend-Formulare sprachlich/visuell verbessern
- Beispiel-Commit: `feat: frontend formuliertexte ueberarbeitet`

Tag 7:
- Aufgabe: API-Client-Skript pruefen und bereinigen
- Beispiel-Commit: `fix: api client ausgaben vereinheitlicht`

Tag 8:
- Aufgabe: README und Checkliste aktualisieren
- Beispiel-Commit: `docs: readme und projekt-checkliste aktualisiert`

Tag 9:
- Aufgabe: Fehlertests ergaenzen
- Beispiel-Commit: `test: negative faelle fuer auth und rezepte ergaenzt`

Tag 10:
- Aufgabe: Demo vorbereiten und letzte Bugs beheben
- Beispiel-Commit: `fix: letzte demo-fehler behoben und abschluss vorbereitet`

## 7. Tagesabschluss (immer)

1. Offene Arbeit committen und pushen.
2. Pull Request erstellen oder aktualisieren.
3. Kurz im Team teilen:
- Was wurde heute gemacht?
- Was ist noch offen?
- Gibt es Blocker?
