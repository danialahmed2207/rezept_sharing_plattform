# Anleitung für Meikel

So machst du täglich einen Commit.

## Einmalig: Repository klonen

```bash
cd Desktop
git clone https://github.com/danialahmed2207/rezept_sharing_plattform.git
cd rezept_sharing_plattform
```

## Täglich: Commit machen

### Schritt 1: Neuen Stand holen
```bash
git checkout main
git pull origin main
```

### Schritt 2: Eigenen Branch erstellen
```bash
git checkout -b feature/meikel-tag-1
```
(Bei Tag 2: `feature/meikel-tag-2`, usw.)

### Schritt 3: Etwas ändern
Öffne die Datei `README.md` und füge unten hinzu:
```
- Meikel - 20.02.2025 - API getestet
```

### Schritt 4: Commit erstellen
```bash
git add README.md
git commit -m "docs: meikel tag 1 - api getestet"
```

### Schritt 5: Hochladen
```bash
git push -u origin feature/meikel-tag-1
```

### Schritt 6: Pull Request
1. Gehe zu github.com/danialahmed2207/rezept_sharing_plattform
2. Klicke auf "Compare & pull request"
3. Erstellen
4. Danial Bescheid sagen

## Fertig!

Wiederhole das jeden Tag mit neuer Tag-Nummer.
