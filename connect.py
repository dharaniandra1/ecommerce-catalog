from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["ecommerceDB"]

products = db["products"]
cart = db["carts"]
orders = db["orders"]
users = db["users"]

print("Connected to MongoDB\n")

# -------------------------------
# Show all products
# -------------------------------
print("Products List:")
for p in products.find({}, {"name": 1, "price": 1, "_id": 0}):
    print(p.get("name", "NoName"), "-", p.get("price", 0))

# -------------------------------
# Total cart price calculation
# -------------------------------
print("\nTotal Cart Price Calculation:")

total = 0

for item in cart.find():

    # skip wrong/empty cart records
    if "productId" not in item:
        continue

    # find product using productId
    product = products.find_one({"_id": ObjectId(item["productId"])})

    if product and "price" in product:
        quantity = item.get("quantity", 1)
        total += product["price"] * quantity

print("Total Cart Price =", total)
