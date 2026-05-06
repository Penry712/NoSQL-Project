from pydantic import BaseModel

class Review(BaseModel):
    user: str
    rating: int
    comment: str

class Product(BaseModel):
    name: str
    brand: str
    category: str
    price: float
    sales_30_days: int = 0
    specs: dict = {}
    rating_avg: float = 0.0
    stock: int = 0
    reviews: list = []