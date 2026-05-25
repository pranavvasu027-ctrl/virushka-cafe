import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["virushka_cafe"]

orders_collection = db["orders"]
counters_collection = db["counters"]