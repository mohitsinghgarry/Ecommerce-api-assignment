from pymongo import MongoClient
from bson import ObjectId
from config import Config 

DB_NAME = "ecommerce"

# print(f"Connecting to MongoDB at {Config.MONGO_URI}")
class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[DB_NAME]
        self.products = self.db.products
        self.orders = self.db.orders


db = Database()

def oid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError