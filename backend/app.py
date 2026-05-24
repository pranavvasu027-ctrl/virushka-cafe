from flask import Flask, request, jsonify
from flask_cors import CORS

# IMPORT DATABASE
from mongo_config import orders_collection

app = Flask(__name__)

# ENABLE CORS
CORS(app)

# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")

def home():

    return "Virushka Cafe Backend Running"


# ==========================================
# PLACE ORDER ROUTE
# ==========================================

@app.route("/place-order", methods=["POST"])

def place_order():

    try:

        data = request.json

        print("\n===== NEW ORDER =====")
        print(data)

        # SAVE TO DATABASE
        orders_collection.insert_one(data)

        print("ORDER SAVED SUCCESSFULLY")

        return jsonify({
            "message": "Order received successfully",
            "success": True
        })

    except Exception as e:

        print("\n===== ERROR =====")
        print(str(e))

        return jsonify({
            "message": str(e),
            "success": False
        }), 500


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)