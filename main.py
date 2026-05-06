from fastapi import FastAPI
from routes import api

app = FastAPI(title="NoSQL-Project", version="1.0.0")
app.include_router(api.router)

@app.get("/")
def root():
    return {"status": "ok"}
