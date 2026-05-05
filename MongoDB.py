from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel

client = MongoClient("mongodb://localhost:27017/")

db = client["NoSQL-Project"]
onlineshop = db["OnlineShop"]