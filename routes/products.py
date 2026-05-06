from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from typing import Optional
from MongoDB import onlineshop
from models import Product, Review

router = APIRouter(prefix="/api/onlineshop", tags=["Products"])

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def list_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = Query(20, le=100),
):
    query = {}
    if category: query["category"] = category
    if brand: query["brand"] = brand
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None: query["price"]["$gte"] = min_price
        if max_price is not None: query["price"]["$lte"] = max_price

    return [serialize(d) for d in onlineshop.find(query).skip(skip).limit(limit)]

@router.get("/{product_id}")
def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(400, "Ungültige ID")
    doc = onlineshop.find_one({"_id": ObjectId(product_id)})
    if not doc:
        raise HTTPException(404, "Produkt nicht gefunden")
    return serialize(doc)

@router.post("/", status_code=201)
def create_product(product: Product):
    result = onlineshop.insert_one(product.model_dump())
    return {"id": str(result.inserted_id)}

@router.put("/{product_id}")
def update_product(product_id: str, product: Product):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(400, "Ungültige ID")
    result = onlineshop.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.model_dump()},
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Produkt nicht gefunden")
    return {"updated": True}

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: str):
    result = onlineshop.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Produkt nicht gefunden")

@router.post("/{product_id}/reviews", status_code=201)
def add_review(product_id: str, review: Review):
    result = onlineshop.update_one(
        {"_id": ObjectId(product_id)},
        {"$push": {"reviews": review.model_dump()}},
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Produkt nicht gefunden")
    return {"added": True}

@router.get("/stats/top-sellers")
def top_sellers(limit: int = 5):
    cursor = onlineshop.find().sort("sales_30_days", -1).limit(limit)
    return [serialize(d) for d in cursor]
