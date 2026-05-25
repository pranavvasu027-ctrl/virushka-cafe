import certifi
from pymongo import MongoClient

# ==========================================
# MONGODB CONNECTION
# ==========================================

client = MongoClient(
    "mongodb+srv://pranavvasu027_db_user:Pranav27@cluster0.icnppne.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tlsCAFile=certifi.where()
)

# ==========================================
# DATABASE
# ==========================================

db = client["virushka_cafe"]

# ==========================================
# COLLECTIONS
# ==========================================

orders_collection   = db["orders"]
counters_collection = db["counters"]   # for auto order numbers
