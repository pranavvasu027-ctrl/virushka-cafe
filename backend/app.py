from flask import Flask, request, jsonify
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime

from mongo_config import orders_collection, counters_collection

app = Flask(__name__)
CORS(app)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return "Virushka Cafe Backend Running"


# ==========================================
# HELPER — get next order number
# ==========================================

def get_next_order_number():

    counter = counters_collection.find_one_and_update(
        {"_id": "orderNumber"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )

    return counter["seq"]


# ==========================================
# PLACE ORDER
# ==========================================

@app.route("/place-order", methods=["POST"])
def place_order():

    try:

        data = request.json

        order_number = get_next_order_number()

        order = {
            "orderNumber": order_number,
            "items": data["items"],
            "totalAmount": data["totalAmount"],
            "transactionId": data["transactionId"],
            "paymentStatus": "Pending Verification",
            "orderStatus": "Waiting For Approval",
            "createdAt": datetime.utcnow()
        }

        result = orders_collection.insert_one(order)

        return jsonify({
            "success": True,
            "message": "Order placed successfully",
            "orderId": str(result.inserted_id),
            "orderNumber": order_number
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

        for order in orders:

            order["_id"] = str(order["_id"])

            if "createdAt" in order and hasattr(order["createdAt"], "isoformat"):

                order["createdAt"] = order["createdAt"].isoformat()

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

        orders_collection.delete_one({
            "_id": ObjectId(order_id)
        })

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
# ANALYTICS
# ==========================================

@app.route("/get-analytics", methods=["GET"])
def get_analytics():

    try:

        pipeline = [

            {
                "$match": {
                    "paymentStatus": "Verified"
                }
            },

            {
                "$addFields": {
                    "date": {
                        "$cond": {
                            "if": {
                                "$ifNull": ["$createdAt", False]
                            },
                            "then": "$createdAt",
                            "else": {
                                "$toDate": "$_id"
                            }
                        }
                    }
                }
            },

            {
                "$group": {
                    "_id": {
                        "year": {
                            "$year": "$date"
                        },
                        "month": {
                            "$month": "$date"
                        }
                    },
                    "revenue": {
                        "$sum": "$totalAmount"
                    },
                    "orderCount": {
                        "$sum": 1
                    }
                }
            },

            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1
                }
            }
        ]

        results = list(
            orders_collection.aggregate(pipeline)
        )

        month_names = [
            "",
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]

        analytics = []

        for r in results:

            analytics.append({
                "label": f"{month_names[r['_id']['month']]} {r['_id']['year']}",
                "revenue": r["revenue"],
                "orderCount": r["orderCount"]
            })

        return jsonify({
            "success": True,
            "data": analytics
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)