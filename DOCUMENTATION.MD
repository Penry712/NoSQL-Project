# Datum: 04.05.2026 1. Doppelstunde

- Informationen zu NoSQL und MongoDB gesammelt
- Planung der Einträge für das Kamera-Sortiment abgeschlossen
- 10 diverse Beispieldatensätze (Systemkameras, Objektive, Zubehör) erstellt
- Implementierung von verschachtelten Arrays (reviews) zur Abbildung von Nutzerbewertungen
- Datenstruktur für Filter- und Sortierfunktionen optimiert (Marke, Bewertung, Sales-Metriken)
- Installation der MongoDB
- Einfügen der KI-Beispielsätze per JSON in MongoDB

#### KI-Nutzung:

- Prompt: „Effiziente NoSQL-Struktur für E-Commerce-Produkte mit Trends“
- Ergebnis zur Validierung der eingebetteten Bewertungsstruktur genutzt
- Prompt: "Erstelle mindestens 10 Beispieldatensätze"
- Ergebnis zur Ersparung von Zeit für Produktinformationen .

# Datum: 04.05.2026 2. Doppelstunde

- Verbindung der Datenbank-Collection mit Python
- Testaufruf der Daten
- Tutorial zur Erstellung einer REST-API in Python angeguckt

#### KI-Nutzung

- Prompt: "Schreibe ein Script in Python zum Auslesen eienr MongoDB"
- Ergebnis: Ein Script, welches eine Verbindung zur MongoDB aufbaut und alle Datensätze ausgibt

# Datum: 05.05.2026 3. Doppelstunde

- Erstellung der REST-API mithilfe von FastAPI und Uvicorn
- Testen der CRUD-Operationen via SwaggerUI welches in FastAPI enthalten ist

#### KI-Nutzung

* Prompt: "Welche Bilbothek zum erstellen einer API in Python sollten wir nutzen?"
* Ergebnis: FastAPI
* Prompt: "Welchen Webserver für FastAPI sollten wir nutzen?"
* Ergebnis: Uvicorn

# Datum 06.05 4.Doppelstunde

- CLI-Tool zur einfachen Benutzung der REST-API implementiert
- CLI-Tool getestet
- Programmcode refactored

#### KI-Nutzung

* Prompt: "Überprüfe unsere CLI Tool und gebe korrigiere ihn gff."
* Ergebnis: Verbesserungen für unseren Code

# Code Dokumentation

- Start des Webservers mit API

  ```
  python -m uvicorn main:app --workers 4
  ```
