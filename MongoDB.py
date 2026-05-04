from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

# Achtung: Bindestrich im Namen!
db = client["NoSQL-Project"]
onlineshop = db["OnlineShop"]

for p in onlineshop.find():
    print(p)