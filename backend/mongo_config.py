from pymongo import MongoClient

# ==========================================
# MONGODB CONNECTION
# ==========================================

client = MongoClient(
    "mongodb+srv://pranavvasu027_db_user:Pranav27@cluster0.icnppne.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# ==========================================
# DATABASE
# ==========================================

db = client["virushka_cafe"]

# ==========================================
# COLLECTION
# ==========================================

orders_collection = db["orders"]