import json
import requests

BASE_URL = "http://localhost:8000/api/onlineshop"

def mache_request(method, path="", data=None, params=None):
    try:
        if method == "GET":
            req = requests.get(BASE_URL + path, params=params)
        elif method == "POST":
            req = requests.post(BASE_URL + path, json=data)
        elif method == "PUT":
            req = requests.put(BASE_URL + path, json=data)
        elif method == "DELETE":
            req = requests.delete(BASE_URL + path)
            
        req.raise_for_status()
        
        if req.content:
            return req.json()
        return None
    except Exception as e:
        print(f"Fehler bei der Verbindung: {e}")
        return None

def zeige_produkt_zeile(product):
    id = product['_id']
    name = product['name']
    marke = product['brand']
    preis = product['price']
    print(f"- [{id}] {name} ({marke}) - {preis} EUR | Bestand: {product['stock']}")

def list_products():
    produkte = mache_request("GET", "/")
    if produkte == None or len(produkte) == 0:
        print("Keine Produkte gefunden.")
    else:
        for p in produkte:
            zeige_produkt_zeile(p)

def get_product():
    productID = input("Produkt-ID eingeben: ")
    produkt = mache_request("GET", f"/{productID}")
    if produkt:
        print(json.dumps(produkt, indent=2))

def create_product():
    neues_produkt = {}
    neues_produkt["name"] = input("Name: ")
    neues_produkt["brand"] = input("Brand: ")
    neues_produkt["category"] = input("Kategorie: ")
    neues_produkt["price"] = float(input("Preis: "))
    neues_produkt["stock"] = int(input("Stock: ") or 0)
    neues_produkt["rating_avg"] = float(input("Rating (0-5): ") or 0)

    antwort = mache_request("POST", "/", data=neues_produkt)
    if antwort:
        print(f"Erfolgreich angelegt mit ID: {antwort['id']}")

def update_product():
    productID = input("Produkt-ID eingeben: ")
    
    update_daten = {}
    update_daten["name"] = input("Neuer Name: ")
    update_daten["brand"] = input("Neue Brand: ")
    update_daten["category"] = input("Neue Kategorie: ")
    update_daten["price"] = float(input("Neuer Preis: "))
    update_daten["stock"] = int(input("Neuer Stock: ") or 0)
    update_daten["rating_avg"] = float(input("Neues Rating (0-5): ") or 0)

    antwort = mache_request("PUT", f"/{productID}", data=update_daten)
    if antwort:
        print("Produkt wurde aktualisiert.")

def delete_product():
    productID = input("Produkt-ID eingeben: ")
    bestaetigung = input("Wirklich loeschen? (j/n): ")
    if bestaetigung == "j":
        mache_request("DELETE", f"/{productID}")
        print("Erfolgreich geloescht.")

def add_review():
    productID = input("Produkt-ID eingeben: ")
    review = {
        "user": input("Benutzername: "),
        "rating": int(input("Rating (1-5): ")),
        "comment": input("Kommentar: ")
    }
    antwort = mache_request("POST", f"/{productID}/reviews", data=review)
    if antwort:
        print("Review wurde hinzugefuegt.")

def list_reviews():
    productID = input("Produkt-ID eingeben: ")
    produkt = mache_request("GET", f"/{productID}")
    
    if produkt:
        reviews = produkt.get("reviews", [])
        if len(reviews) == 0:
            print("Dieses Produkt hat noch keine Reviews.")
        else:
            print(f"\nReviews fuer '{produkt['name']}':")
            for r in reviews:
                sterne = "*" * r["rating"]
                print(f"  [{sterne}] {r['user']}: {r['comment']}")

def top_sellers():
    limit_input = input("Wie viele anzeigen? (Standard 5): ")
    limit = int(limit_input) if limit_input else 5
    
    produkte = mache_request("GET", "/stats/top-sellers", params={"limit": limit})
    if produkte:
        print(f"\n--- Top {len(produkte)} Seller ---")
        platz = 1
        for p in produkte:
            verkauft = p.get('sales_30_days', 0)
            print(f"{platz}. {p['name']} ({p['brand']}) - {verkauft} mal verkauft")
            platz += 1

def menu():
    # Klassisches Anfänger-Menü mit while-Schleife und if/elif
    while True:
        print("\n=== OnlineShop CLI ===")
        print("1) Alle Produkte auflisten")
        print("2) Einzelnes Produkt anzeigen")
        print("3) Produkt anlegen")
        print("4) Produkt aktualisieren")
        print("5) Produkt loeschen")
        print("6) Review hinzufuegen")
        print("7) Reviews zu Produkt anzeigen")
        print("8) Top-Seller anzeigen")
        print("0) Beenden")
        
        auswahl = input("Bitte Nummer auswaehlen: ")
        
        if auswahl == "1":
            list_products()
        elif auswahl == "2":
            get_product()
        elif auswahl == "3":
            create_product()
        elif auswahl == "4":
            update_product()
        elif auswahl == "5":
            delete_product()
        elif auswahl == "6":
            add_review()
        elif auswahl == "7":
            list_reviews()
        elif auswahl == "8":
            top_sellers()
        elif auswahl == "0":
            print("Programm wird beendet.")
            break
        else:
            print("Unbekannte Auswahl, bitte nochmal versuchen.")

if __name__ == "__main__":
    menu()