from fastapi import FastAPI, HTTPException
from bson import ObjectId
from MongoDB import collection
from models import Product, Review

app = FastAPI(title="NoSQL-Project", version="1.0.0")

# Hilfsfunktion, um die MongoDB-ID in einen normalen String umzuwandeln,
# da FastAPI sonst Fehler beim Anzeigen im Browser wirft.
def serialize(dokument):
    dokument["_id"] = str(dokument["_id"])
    return dokument

@app.get("/")
def root():
    return {"status": "ok", "message": "Willkommen zur API"}

@app.get("/api/onlineshop")
def list_products(category: str = None, brand: str = None):
    # Einfache Suche aufbauen
    such_filter = {}
    if category != None: 
        such_filter["category"] = category
    if brand != None: 
        such_filter["brand"] = brand

    produkte = collection.find(such_filter)
    
    ergebnis_liste = []
    for p in produkte:
        ergebnis_liste.append(serialize(p))
        
    return ergebnis_liste

@app.get("/api/onlineshop/stats/top-sellers")
def top_sellers(limit: int = 5):
    # Sortiert nach sales_30_days absteigend (-1)
    cursor = collection.find().sort("sales_30_days", -1).limit(limit)
    
    ergebnis_liste = []
    for d in cursor:
        ergebnis_liste.append(serialize(d))
    return ergebnis_liste

@app.get("/api/onlineshop/{product_id}")
def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(400, "Ungültige ID")
        
    doc = collection.find_one({"_id": ObjectId(product_id)})
    if doc == None:
        raise HTTPException(404, "Produkt nicht gefunden")
        
    return serialize(doc)

@app.post("/api/onlineshop", status_code=201)
def create_product(product: Product):
    # .dict() wandelt das Pydantic-Modell in ein normales Dictionary um
    result = collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@app.put("/api/onlineshop/{product_id}")
def update_product(product_id: str, product: Product):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(400, "Ungültige ID")
        
    result = collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Produkt nicht gefunden")
        
    return {"updated": True}

@app.delete("/api/onlineshop/{product_id}", status_code=204)
def delete_product(product_id: str):
    result = collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Produkt nicht gefunden")

@app.post("/api/onlineshop/{product_id}/reviews", status_code=201)
def add_review(product_id: str, review: Review):
    result = collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$push": {"reviews": review.dict()}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Produkt nicht gefunden")
        
    return {"added": True}