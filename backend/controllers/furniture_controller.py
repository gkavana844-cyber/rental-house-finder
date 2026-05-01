from flask import current_app, request
from datetime import datetime
import cloudinary.uploader


# =========================
# ✅ ADD FURNITURE (UPDATED)
# =========================
def add_furniture():
    db = current_app.db

    data = request.form   # 🔥 form-data
    file = request.files.get("image")  # 🔥 image file

    name = data.get("name")
    price = data.get("price")
    contact = data.get("contact")

    # =========================
    # ✅ VALIDATION
    # =========================
    if not name or not price or not contact:
        return {"success": False, "error": "All fields required"}

    try:
        price = int(price)
    except:
        return {"success": False, "error": "Invalid price"}

    # =========================
    # 🖼 IMAGE UPLOAD
    # =========================
    image_url = None

    try:
        if file and file.filename != "":
            result = cloudinary.uploader.upload(file)
            print("🔥 Cloudinary Upload:", result)
            image_url = result.get("secure_url")
    except Exception as e:
        print("❌ Image Upload Error:", e)
        return {"success": False, "error": "Image upload failed"}

    # =========================
    # ✅ FINAL OBJECT
    # =========================
    furniture = {
        "name": name,
        "price": price,
        "contact": contact,
        "image": image_url,  # ✅ stored URL
        "created_at": datetime.utcnow()
    }

    try:
        result = db.furniture.insert_one(furniture)

        return {
            "success": True,
            "message": "Furniture added ✅",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        print("❌ DB ERROR:", e)
        return {"success": False, "error": "Database error"}


# =========================
# ✅ GET ALL FURNITURE
# =========================
def get_furniture():
    db = current_app.db

    data = []

    for item in db.furniture.find().sort("created_at", -1):
        item["_id"] = str(item["_id"])
        data.append(item)

    return {
        "success": True,
        "data": data
    }