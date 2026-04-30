from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
import re

house_bp = Blueprint("house", __name__)


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
# ✅ ADD HOUSE
# =========================
@house_bp.route("/add", methods=["POST"])
def add_house():
    db = current_app.db

    try:
        # 🔥 IMPORTANT: use form-data instead of JSON
        data = request.form
        files = request.files.getlist("images")

        print("🔥 FULL FORM:", dict(data))
        print("🔥 FILE COUNT:", len(files))

        # =========================
        # ✅ REQUIRED
        # =========================
        title = data.get("title")
        location = data.get("location")

        if not title:
            return jsonify({"error": "Title required"}), 400

        if not location or location.strip() == "":
            return jsonify({"error": "Location required"}), 400

        # =========================
        # ✅ TYPE
        # =========================
        house_type = data.get("type", "rent")

        if house_type not in ["rent", "lease"]:
            return jsonify({"error": "Invalid house type"}), 400

        price = data.get("price")
        lease_duration = data.get("lease_duration")

        # =========================
        # 💰 RENT / LEASE
        # =========================
        if house_type == "rent":
            if not price:
                return jsonify({"error": "Monthly rent required"}), 400

            try:
                price = int(price)
            except:
                return jsonify({"error": "Invalid price"}), 400

            lease_duration = None

        elif house_type == "lease":
            if not lease_duration:
                return jsonify({"error": "Lease duration required"}), 400

            try:
                lease_duration = int(lease_duration)
            except:
                return jsonify({"error": "Invalid lease duration"}), 400

            price = None

        # =========================
        # 📞 PHONE
        # =========================
        phone = clean_number(data.get("phone"))
        whatsapp = clean_number(data.get("whatsapp"))

        if not phone or len(phone) != 10:
            return jsonify({"error": "Invalid phone number"}), 400

        if whatsapp and len(whatsapp) != 10:
            return jsonify({"error": "Invalid WhatsApp number"}), 400

        # =========================
        # 🧾 AMENITIES
        # =========================
        amenities = data.get("amenities", "")
        if isinstance(amenities, str):
            amenities = [a.strip() for a in amenities.split(",") if a.strip()]

        # =========================
        # 🖼 IMAGE UPLOAD (OPTIONAL)
        # =========================
        image_urls = []

        for file in files:
            if file and file.filename != "":
                # If using cloudinary → keep your old logic
                # For now just store filename (safe fallback)
                image_urls.append(file.filename)

        # =========================
        # 📍 MAP
        # =========================
        try:
            latitude = float(data.get("latitude")) if data.get("latitude") else None
            longitude = float(data.get("longitude")) if data.get("longitude") else None
        except:
            latitude = None
            longitude = None

        # =========================
        # 🧹 CLEAN LOCATION
        # =========================
        location = str(location).strip()

        # =========================
        # ✅ FINAL OBJECT
        # =========================
        house = {
            "title": title,
            "location": location,
            "type": house_type,

            "price": price,
            "lease_duration": lease_duration,

            "images": image_urls,
            "amenities": amenities,

            "latitude": latitude,
            "longitude": longitude,

            "phone": phone,
            "whatsapp": whatsapp,

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        print("✅ SAVING:", house)

        result = db.houses.insert_one(house)

        return jsonify({
            "message": "House added successfully ✅",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500
    
# =========================
# ✅ GET / SEARCH HOUSES
# =========================
@house_bp.route("/", methods=["GET"])
def get_houses():
    db = current_app.db

    location = request.args.get("location")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    query = {}

    if location:
        query["location"] = {"$regex": location, "$options": "i"}

    if min_price or max_price:
        query["price"] = {}

        if min_price:
            query["price"]["$gte"] = int(min_price)

        if max_price:
            query["price"]["$lte"] = int(max_price)

    houses = list(db.houses.find(query).sort("created_at", -1))

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
        return jsonify({
            "success": False,
            "error": "Invalid ID"
        }), 400

    if not house:
        return jsonify({
            "success": False,
            "error": "House not found"
        }), 404

    house["_id"] = str(house["_id"])

    return jsonify({
        "success": True,
        "data": house
    })