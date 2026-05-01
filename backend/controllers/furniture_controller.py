from flask import request, current_app
from models.furniture_model import create_furniture


def add_furniture():
    db = current_app.db
    data = request.json

    result = create_furniture(data)

    if not result["success"]:
        return result

    furniture = result["data"]

    try:
        inserted = db.furniture.insert_one(furniture)

        return {
            "success": True,
            "message": "Furniture added ✅",
            "id": str(inserted.inserted_id)
        }

    except Exception as e:
        print("❌ DB ERROR:", e)
        return {"success": False, "error": "Database error"}