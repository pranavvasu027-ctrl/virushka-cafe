from flask import Flask, request, jsonify
from flask_cors import CORS

from mongo_config import orders_collection

from bson.objectid import ObjectId

app = Flask(__name__)

# ==========================================
# ENABLE CORS
# ==========================================

CORS(app)

# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")

def home():

    return "Virushka Cafe Backend Running"


# ==========================================
# PLACE ORDER
# ==========================================

@app.route("/place-order", methods=["POST"])

def place_order():

    try:

        data = request.json

        # ORDER DATA

        order = {

            "items": data["items"],

            "totalAmount": data["totalAmount"],

            "transactionId": data["transactionId"],

            "paymentStatus": "Pending Verification",

            "orderStatus": "Waiting For Approval"
        }

        # INSERT INTO MONGODB

        result = orders_collection.insert_one(order)

        return jsonify({

            "success": True,

            "message": "Order placed successfully",

            "orderId": str(result.inserted_id)
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        })


# ==========================================
# GET ALL ORDERS
# ==========================================

@app.route("/get-orders", methods=["GET"])

def get_orders():

    try:

        orders = list(orders_collection.find())

        # CONVERT OBJECT ID TO STRING

        for order in orders:

            order["_id"] = str(order["_id"])

        return jsonify(orders)

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        })


# ==========================================
# VERIFY ORDER
# ==========================================

@app.route("/verify-order", methods=["POST"])

def verify_order():

    try:

        data = request.json

        order_id = data["orderId"]

        orders_collection.update_one(

            {"_id": ObjectId(order_id)},

            {
                "$set": {

                    "paymentStatus": "Verified",

                    "orderStatus": "Preparing"
                }
            }
        )

        return jsonify({

            "success": True,

            "message": "Order verified successfully"
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        })


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.route("/update-status", methods=["POST"])

def update_status():

    try:

        data = request.json

        order_id = data["orderId"]

        new_status = data["status"]

        orders_collection.update_one(

            {"_id": ObjectId(order_id)},

            {
                "$set": {

                    "orderStatus": new_status
                }
            }
        )

        return jsonify({

            "success": True,

            "message": "Status updated successfully"
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        })


# ==========================================
# DELETE ORDER
# ==========================================

@app.route("/delete-order", methods=["POST"])

def delete_order():

    try:

        data = request.json

        order_id = data["orderId"]

        orders_collection.delete_one(

            {"_id": ObjectId(order_id)}
        )

        return jsonify({

            "success": True,

            "message": "Order deleted successfully"
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)
        })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)