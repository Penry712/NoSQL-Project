"""
setup_db.py
Erstellt (falls nicht vorhanden) die Datenbank 'NoSQL-Project' mit der
Collection 'OnlineShop' und importiert die Daten aus 'data.json'.
"""

import json
from pymongo import MongoClient

# --- Konfiguration ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "NoSQL-Project"
COLLECTION_NAME = "OnlineShop"
JSON_FILE = "data.json"


def main():
    # 1. Verbindung herstellen
    client = MongoClient(MONGO_URI)
    print(f"✅ Verbunden mit {MONGO_URI}")

    # 2. Datenbank prüfen / anlegen
    if DB_NAME in client.list_database_names():
        print(f"ℹ️  Datenbank '{DB_NAME}' existiert bereits.")
    else:
        print(f"🆕 Datenbank '{DB_NAME}' wird beim ersten Insert erstellt.")
    db = client[DB_NAME]

    # 3. Collection prüfen / anlegen
    if COLLECTION_NAME in db.list_collection_names():
        print(f"ℹ️  Collection '{COLLECTION_NAME}' existiert bereits.")
    else:
        db.create_collection(COLLECTION_NAME)
        print(f"🆕 Collection '{COLLECTION_NAME}' wurde erstellt.")
    collection = db[COLLECTION_NAME]

    # 4. JSON-Datei einlesen
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Datei '{JSON_FILE}' nicht gefunden.")
        return

    if not isinstance(data, list):
        data = [data]  # einzelnes Objekt in Liste packen
    print(f"📄 {len(data)} Einträge aus '{JSON_FILE}' geladen.")

    # 5. Doppelte Einträge vermeiden (anhand 'name')
    new_items = []
    for item in data:
        if "name" in item and collection.find_one({"name": item["name"]}):
            print(f"  ⏭️  Übersprungen (existiert): {item['name']}")
        else:
            new_items.append(item)

    # 6. Einfügen
    if new_items:
        result = collection.insert_many(new_items)
        print(f"✅ {len(result.inserted_ids)} neue Dokumente eingefügt.")
    else:
        print("ℹ️  Keine neuen Dokumente zum Einfügen.")

    # 7. Status
    total = collection.count_documents({})
    print(f"📦 Gesamt in '{DB_NAME}.{COLLECTION_NAME}': {total} Dokumente")

    client.close()


if __name__ == "__main__":
    main()
