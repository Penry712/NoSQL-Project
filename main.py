from fastapi import FastAPI
from routes import products

app = FastAPI(title="NoSQL-Project", version="1.0.0")
app.include_router(products.router)

@app.get("/")
def root():
    return {"status": "ok"}
