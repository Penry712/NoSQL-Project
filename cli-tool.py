import json
import requests

BASE_URL = "http://localhost:8000/api/onlineshop"


def request(method, path="", data=None, params=None):
    try:
        resp = requests.request(method, BASE_URL + path, json=data, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json() if resp.content else None
    except requests.HTTPError as e:
        print(f"Fehler {e.response.status_code}: {e.response.text}")
    except requests.RequestException as e:
        print(f"Verbindungsfehler: {e}")
    return None


def _print_product_line(p):
    print(f"- [{p['_id']}] {p['name']} ({p['brand']}) - {p['price']} EUR | Stock: {p['stock']} | Sales 30d: {p.get('sales_30_days', 0)}")


def list_products():
    products = request("GET", "/")
    if not products:
        print("Keine Produkte gefunden.")
        return
    for p in products:
        _print_product_line(p)


def get_product():
    pid = input("Produkt-ID: ").strip()
    p = request("GET", f"/{pid}")
    if p:
        print(json.dumps(p, indent=2, ensure_ascii=False))


def _read_product():
    return {
        "name":       input("Name: ").strip(),
        "brand":      input("Brand: ").strip(),
        "category":   input("Kategorie: ").strip(),
        "price":      float(input("Preis: ")),
        "stock":      int(input("Stock: ") or 0),
        "rating_avg": float(input("Rating (0-5): ") or 0),
    }


def create_product():
    res = request("POST", "/", _read_product())
    if res:
        print(f"Angelegt mit ID: {res['id']}")


def update_product():
    pid = input("Produkt-ID: ").strip()
    res = request("PUT", f"/{pid}", _read_product())
    if res:
        print("Aktualisiert.")


def delete_product():
    pid = input("Produkt-ID: ").strip()
    if input("Wirklich loeschen? (j/N): ").lower() == "j":
        request("DELETE", f"/{pid}")
        print("Geloescht.")


def add_review():
    pid = input("Produkt-ID: ").strip()
    review = {
        "user":    input("Benutzer: ").strip(),
        "rating":  int(input("Rating (1-5): ")),
        "comment": input("Kommentar: ").strip(),
    }
    res = request("POST", f"/{pid}/reviews", review)
    if res:
        print("Review hinzugefuegt.")


def list_reviews():
    pid = input("Produkt-ID: ").strip()
    p = request("GET", f"/{pid}")
    if not p:
        return
    reviews = p.get("reviews", [])
    if not reviews:
        print("Keine Reviews vorhanden.")
        return
    print(f"\n{len(reviews)} Review(s) fuer '{p['name']}':")
    for r in reviews:
        stars = "*" * r["rating"] + "-" * (5 - r["rating"])
        print(f"  [{stars}] {r['user']}: {r['comment']}")


def top_sellers():
    raw = input("Anzahl (Default 5): ").strip()
    limit = int(raw) if raw else 5
    products = request("GET", "/stats/top-sellers", params={"limit": limit})
    if not products:
        print("Keine Daten.")
        return
    print(f"\n--- Top {len(products)} Seller (30 Tage) ---")
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['name']} ({p['brand']}) - {p.get('sales_30_days', 0)} verkauft | {p['price']} EUR")


def menu():
    actions = {
        "1": ("Alle Produkte auflisten",    list_products),
        "2": ("Einzelnes Produkt anzeigen", get_product),
        "3": ("Produkt anlegen",            create_product),
        "4": ("Produkt aktualisieren",      update_product),
        "5": ("Produkt loeschen",           delete_product),
        "6": ("Review hinzufuegen",         add_review),
        "7": ("Reviews zu Produkt anzeigen",list_reviews),
        "8": ("Top-Seller anzeigen",        top_sellers),
        "0": ("Beenden",                    None),
    }
    while True:
        print("\n--- OnlineShop CLI ---")
        for k, (label, _) in actions.items():
            print(f"  {k}) {label}")
        choice = input("Auswahl: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action and action[1]:
            try:
                action[1]()
            except ValueError as e:
                print(f"Ungueltige Eingabe: {e}")
        else:
            print("Unbekannte Auswahl.")


if __name__ == "__main__":
    menu()