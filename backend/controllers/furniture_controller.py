from flask import current_app
from datetime import datetime

def add_furniture(data):
    db = current_app.db

    name = data.get("name")
    price = data.get("price")
    contact = data.get("contact")

    if not name or not price or not contact:
        return {"success": False, "error": "All fields required"}

    furniture = {
        "name": name,
        "price": int(price),
        "contact": contact,
        "created_at": datetime.utcnow()
    }

    result = db.furniture.insert_one(furniture)

    return {
        "success": True,
        "message": "Furniture added ✅",
        "id": str(result.inserted_id)
    }


def get_furniture():
    db = current_app.db

    data = []
    for item in db.furniture.find():
        item["_id"] = str(item["_id"])
        data.append(item)

    return {"success": True, "data": data}