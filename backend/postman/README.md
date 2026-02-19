# Postman Collection

Diese Collection enthaelt alle API-Endpunkte der Rezept Sharing Plattform.

## Importieren

1. Postman oeffnen
2. Auf "Import" klicken
3. Die Datei `Rezept_Sharing_API.postman_collection.json` auswaehlen

## Umgebungsvariablen

Die Collection verwendet folgende Variablen:

| Variable | Standardwert | Beschreibung |
|----------|--------------|--------------|
| `base_url` | `http://127.0.0.1:5000/api` | API Basis-URL |
| `token` | - | JWT-Token (wird automatisch gesetzt) |

### Umgebung erstellen:

1. In Postman auf das Zahnrad (Environments) klicken
2. "Create Environment" waehlen
3. Name: "Rezept Sharing Local"
4. Variablen hinzufuegen:
   - `base_url`: `http://127.0.0.1:5000/api`
   - `token`: (leer lassen)
5. Speichern und als aktiv setzen

## Verwendung

### 1. Health Check

Sende den "Health Check" Request um zu pruefen ob die API laeuft.

### 2. Registrierung

Sende den "Register" Request mit deinen Daten.

### 3. Login

Sende den "Login" Request. Der Token wird automatisch in der Umgebungsvariable `token` gespeichert.

### 4. Geschuetzte Endpunkte

Alle Requests mit `{{token}}` verwenden den gespeicherten Token automatisch.

## Ablauf

Empfohlene Reihenfolge zum Testen:

1. **Health** → Health Check
2. **Auth** → Register
3. **Auth** → Login (speichert Token)
4. **Recipes** → Create Recipe
5. **Recipes** → List All Recipes
6. **Comments** → Create Comment
7. **Favorites** → Add Favorite
8. **Favorites** → List Favorites

## Tipps

- Nach dem Login wird der Token automatisch gespeichert
- Alle geschuetzten Endpunkte verwenden den gespeicherten Token
- Die ID in URLs (z.B. `/recipes/1`) muss ggf. angepasst werden
