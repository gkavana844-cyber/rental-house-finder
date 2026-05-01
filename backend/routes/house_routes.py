from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
import re
import cloudinary
import cloudinary.uploader
import os

# ✅ CREATE BLUEPRINT
house_bp = Blueprint("house", __name__)

# 🔥 CLOUDINARY CONFIG
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("CLOUD_API_KEY"),
    api_secret=os.environ.get("CLOUD_API_SECRET"),
    secure=True
)

# =========================
# 📞 CLEAN NUMBER
# =========================
def clean_number(num):
    if not num:
        return None

    digits = re.sub(r"\D", "", num)

    if digits.startswith("91"):
        digits = digits[2:]

    return digits


# =========================
# ✅ ADD HOUSE (FIXED)
# =========================
@house_bp.route("/add", methods=["POST"])
def add_house():
    db = current_app.db

    try:
        data = request.form
        files = request.files.getlist("images")

        print("🔥 FILES RECEIVED:", files)

        title = data.get("title")
        location = data.get("location")

        if not title:
            return jsonify({"error": "Title required"}), 400

        if not location:
            return jsonify({"error": "Location required"}), 400

        house_type = data.get("type", "rent")

        price = data.get("price")
        lease_duration = data.get("lease_duration")

        if house_type == "rent":
            if not price:
                return jsonify({"error": "Monthly rent required"}), 400
            price = int(price)
            lease_duration = None

        elif house_type == "lease":
            if not lease_duration:
                return jsonify({"error": "Lease duration required"}), 400
            lease_duration = int(lease_duration)
            price = None

        phone = clean_number(data.get("phone"))
        whatsapp = clean_number(data.get("whatsapp"))

        if not phone or len(phone) != 10:
            return jsonify({"error": "Invalid phone number"}), 400

        if whatsapp and len(whatsapp) != 10:
            return jsonify({"error": "Invalid WhatsApp number"}), 400

        amenities = data.get("amenities", "")
        amenities = [a.strip() for a in amenities.split(",") if a.strip()]

        # 🔥 CLOUDINARY IMAGE UPLOAD
        image_urls = []

        for file in files:
            if file and file.filename != "":
                result = cloudinary.uploader.upload(file)

                print("🔥 CLOUDINARY RESULT:", result)

                image_urls.append(result["secure_url"])  # ✅ FIXED

        latitude = float(data.get("latitude")) if data.get("latitude") else None
        longitude = float(data.get("longitude")) if data.get("longitude") else None

        house = {
            "title": title,
            "location": location.strip(),
            "type": house_type,
            "price": price,
            "lease_duration": lease_duration,
            "images": image_urls,  # ✅ NOW URL
            "amenities": amenities,
            "latitude": latitude,
            "longitude": longitude,
            "phone": phone,
            "whatsapp": whatsapp,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = db.houses.insert_one(house)

        return jsonify({
            "message": "House added successfully ✅",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


# =========================
# ✅ GET HOUSES
# =========================
@house_bp.route("/", methods=["GET"])
def get_houses():
    db = current_app.db

    houses = list(db.houses.find().sort("created_at", -1))

    for h in houses:
        h["_id"] = str(h["_id"])

    return jsonify({
        "success": True,
        "data": houses
    })


# =========================
# ✅ GET SINGLE HOUSE
# =========================
@house_bp.route("/<id>", methods=["GET"])
def get_house(id):
    db = current_app.db

    try:
        house = db.houses.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid ID"}), 400

    if not house:
        return jsonify({"error": "House not found"}), 404

    house["_id"] = str(house["_id"])

    return jsonify({
        "success": True,
        "data": house
    })