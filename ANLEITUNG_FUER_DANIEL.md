# Anleitung für Daniel - Tägliche Commits

Hallo Daniel! 😊

Hier ist deine Schritt-für-Schritt Anleitung, wie du jeden Tag einen Commit machst.

---

## Vorbereitung (einmalig am Anfang)

### 1. Repository klonen

Öffne das Terminal (Command Prompt auf Windows, Terminal auf Mac) und gib ein:

```bash
cd Desktop
git clone https://github.com/danialahmed2207/rezept_sharing_plattform.git
cd rezept_sharing_plattform
```

### 2. Einrichtung testen

```bash
git status
```

Du solltest sehen: "On branch main"

---

## Täglicher Ablauf (für die nächsten 5-6 Tage)

### Schritt 1: Aktuellen Stand holen (JEDEN TAG!)

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
```

> ⚠️ **Wichtig:** Mach das immer als ERSTES, bevor du anfängst!

---

### Schritt 2: Eigenen Branch erstellen

```bash
git checkout -b feature/daniel-tag-X
```

> Ersetze **X** mit der Nummer des Tages (1, 2, 3, 4, 5, 6)

**Beispiele:**
- Tag 1: `git checkout -b feature/daniel-tag-1`
- Tag 2: `git checkout -b feature/daniel-tag-2`
- Tag 3: `git checkout -b feature/daniel-tag-3`

---

### Schritt 3: Eine kleine Änderung machen

**Wähle EINE dieser Optionen:**

#### Option A: Kommentar zu README hinzufügen

Öffne die Datei `README.md` und füge am Ende hinzu:

```markdown
## Team-Mitglied

- **Daniel** - [Datum] - [Kurze Beschreibung was du gemacht hast]
```

**Beispiel:**
```markdown
## Team-Mitglied

- **Daniel** - 2025-02-20 - API-Tests durchgeführt
```

#### Option B: Datei erstellen

Erstelle eine neue Datei `daniel-notizen.txt`:

```bash
# Auf Windows:
echo "Daniel - Tag X - [Beschreibung]" > daniel-notizen.txt

# Auf Mac:
echo "Daniel - Tag X - [Beschreibung]" > daniel-notizen.txt
```

#### Option C: Kleinere Code-Änderung

- Rechtschreibfehler korrigieren
- Kommentar hinzufügen
- Formatierung verbessern

---

### Schritt 4: Änderungen speichern (Commit)

```bash
# Alle Änderungen zur Staging-Area hinzufügen
git add .

# Commit erstellen
git commit -m "docs: daniel tag X - [kurze Beschreibung]"
```

**Beispiele für Commit Messages:**

```bash
# Tag 1:
git commit -m "docs: daniel tag 1 - readme um team-info erweitert"

# Tag 2:
git commit -m "docs: daniel tag 2 - api getestet und notizen erstellt"

# Tag 3:
git commit -m "docs: daniel tag 3 - rechtschreibfehler korrigiert"

# Tag 4:
git commit -m "docs: daniel tag 4 - kommentare hinzugefuegt"

# Tag 5:
git commit -m "docs: daniel tag 5 - tests durchgefuehrt"

# Tag 6:
git commit -m "docs: daniel tag 6 - finale dokumentation"
```

---

### Schritt 5: Auf GitHub hochladen

```bash
git push -u origin feature/daniel-tag-X
```

> Ersetze **X** mit der Tag-Nummer

---

### Schritt 6: Pull Request erstellen (auf GitHub)

1. Gehe zu: https://github.com/danialahmed2207/rezept_sharing_plattform
2. Klicke auf den grünen Button "Compare & pull request"
3. Titel: `Daniel Tag X - [Beschreibung]`
4. Klicke auf "Create pull request"
5. Sag Danial Bescheid, dass er mergen soll

---

## Komplette Beispiele für jeden Tag

### 🔵 TAG 1

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
git checkout -b feature/daniel-tag-1

# Öffne README.md und füge hinzu:
# ## Team
# - Daniel - 2025-02-20 - Projekt-Setup verstanden

git add .
git commit -m "docs: daniel tag 1 - team-info hinzugefuegt"
git push -u origin feature/daniel-tag-1
```

Dann auf GitHub Pull Request erstellen.

---

### 🟢 TAG 2

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
git checkout -b feature/daniel-tag-2

# Teste die API oder mache eine kleine Änderung
echo "Daniel - API-Tests durchgefuehrt" > daniel-tests.txt

git add .
git commit -m "docs: daniel tag 2 - api-tests dokumentiert"
git push -u origin feature/daniel-tag-2
```

---

### 🟡 TAG 3

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
git checkout -b feature/daniel-tag-3

# Korrigiere einen Rechtschreibfehler in README.md
# Oder füge einen Kommentar hinzu

git add .
git commit -m "docs: daniel tag 3 - rechtschreibfehler korrigiert"
git push -u origin feature/daniel-tag-3
```

---

### 🟠 TAG 4

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
git checkout -b feature/daniel-tag-4

# Füge Dokumentation hinzu
echo "Daniel - Code-Review durchgefuehrt" > daniel-review.txt

git add .
git commit -m "docs: daniel tag 4 - code-review dokumentiert"
git push -u origin feature/daniel-tag-4
```

---

### 🔴 TAG 5

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
git checkout -b feature/daniel-tag-5

# Führe Tests durch und dokumentiere
git add .
git commit -m "docs: daniel tag 5 - tests dokumentiert"
git push -u origin feature/daniel-tag-5
```

---

### 🟣 TAG 6 (Optional)

```bash
cd Desktop/rezept_sharing_plattform
git checkout main
git pull origin main
git checkout -b feature/daniel-tag-6

git add .
git commit -m "docs: daniel tag 6 - finale tests"
git push -u origin feature/daniel-tag-6
```

---

## WICHTIGE REGELN

| ✅ Richtig | ❌ Falsch |
|-----------|-----------|
| Jeden Tag ein Commit | Alles auf einmal committen |
| Kleine Änderungen | Große Refactorings |
| Branch erstellen | Direkt auf main arbeiten |
| `git pull` vorher | Ohne pull anfangen |
| Danial informieren | Pull Request vergessen |

---

## Hilfe

Wenn etwas nicht funktioniert:

1. **Konflikt?** → Sag Danial sofort Bescheid
2. **Fehler?** → Kopiere die Fehlermeldung und schick sie Danial
3. **Unsicher?** → Frag Danial vor dem Commit

---

## Schnell-Checkliste

- [ ] `git checkout main`
- [ ] `git pull origin main`
- [ ] `git checkout -b feature/daniel-tag-X`
- [ ] Änderung machen
- [ ] `git add .`
- [ ] `git commit -m "docs: daniel tag X - ..."`
- [ ] `git push -u origin feature/daniel-tag-X`
- [ ] Pull Request auf GitHub erstellen
- [ ] Danial Bescheid sagen

---

## Unterschied zu Meikel

Ihr macht beide das Gleiche, aber:
- **Meikel** nutzt: `feature/meikel-tag-1`, `feature/meikel-tag-2`, ...
- **Daniel** nutzt: `feature/daniel-tag-1`, `feature/daniel-tag-2`, ...

So habt ihr getrennte Branches und keine Konflikte!

---

**Viel Erfolg! 🚀**

Bei Fragen einfach Danial fragen.
