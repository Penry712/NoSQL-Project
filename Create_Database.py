import json
from pymongo import MongoClient

def main():
    # 1. Verbindung herstellen
    print("Verbinde mit lokaler MongoDB...")
    client = MongoClient("mongodb://localhost:27017/")
    
    db = client["NoSQL-Project"]
    collection = db["OnlineShop"]

    # 2. JSON-Datei einlesen
    print("Lese data.json ein...")
    try:
        datei = open("data.json", "r", encoding="utf-8")
        daten = json.load(datei)
        datei.close()
    except FileNotFoundError:
        print("Fehler: Datei 'data.json' wurde nicht gefunden.")
        return

    # 3. Einfügen der Daten mit Prüfung
    neue_eintraege = 0
    uebersprungen = 0

    for item in daten:
        # Prüfen ob das Produkt schon existiert
        existiert_schon = collection.find_one({"name": item["name"]})
        
        if existiert_schon:
            print(f"Uebersprungen: {item['name']} (gibt es schon)")
            uebersprungen += 1
        else:
            collection.insert_one(item)
            neue_eintraege += 1

    # 4. Zusammenfassung
    print("\n--- Zusammenfassung ---")
    print(f"Neu eingefuegt: {neue_eintraege}")
    print(f"Uebersprungen: {uebersprungen}")
    print(f"Gesamt in der Datenbank: {collection.count_documents({})}")

if __name__ == "__main__":
    main()