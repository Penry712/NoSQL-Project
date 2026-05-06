from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Review(BaseModel):
    user: str
    rating: int = Field(ge=1, le=5)
    comment: str

class Product(BaseModel):
    name: str
    brand: str
    category: str
    price: float = Field(gt=0)
    sales_30_days: int = 0
    specs: Dict[str, Any] = {}
    rating_avg: float = Field(ge=0, le=5)
    stock: int = 0
    reviews: List[Review] = []

class ProductOut(Product):
    id: str = Field(alias="_id")