from flask import current_app, request, jsonify
from datetime import datetime
import re
import cloudinary
import cloudinary.uploader
import os

# 🔥 CLOUDINARY CONFIG
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)


def add_house():
    db = current_app.db

    data = request.form  # 🔥 form-data
    files = request.files.getlist("images")  # 🔥 images

    print("🔥 Incoming Data:", data)

    # =========================
    # ✅ REQUIRED VALIDATION
    # =========================
    title = data.get("title")
    location = data.get("location")

    if not title or not location:
        return jsonify({"success": False, "error": "Title and Location are required"}), 400

    # =========================
    # ✅ TYPE
    # =========================
    house_type = data.get("type", "rent")

    if house_type not in ["rent", "lease"]:
        return jsonify({"success": False, "error": "Invalid house type"}), 400

    # =========================
    # 💰 PRICE / LEASE
    # =========================
    price = data.get("price")
    lease_duration = data.get("lease_duration")

    if house_type == "rent":
        if not price:
            return jsonify({"success": False, "error": "Monthly rent required"}), 400

        try:
            price = int(price)
        except:
            return jsonify({"success": False, "error": "Invalid price"}), 400

        lease_duration = None

    elif house_type == "lease":
        if not lease_duration:
            return jsonify({"success": False, "error": "Lease duration required"}), 400

        try:
            lease_duration = int(lease_duration)
        except:
            return jsonify({"success": False, "error": "Invalid lease duration"}), 400

        price = None

    # =========================
    # 📞 PHONE + WHATSAPP
    # =========================
    phone = data.get("phone")
    whatsapp = data.get("whatsapp")

    def clean_number(num):
        if not num:
            return None

        digits = re.sub(r"\D", "", num)

        if digits.startswith("91"):
            digits = digits[2:]

        return digits

    phone = clean_number(phone)
    whatsapp = clean_number(whatsapp)

    if not phone or len(phone) != 10:
        return jsonify({"success": False, "error": "Invalid phone number"}), 400

    if whatsapp and len(whatsapp) != 10:
        return jsonify({"success": False, "error": "Invalid WhatsApp number"}), 400

    # =========================
    # 🧾 AMENITIES
    # =========================
    amenities = data.get("amenities", [])
    if isinstance(amenities, str):
        amenities = [a.strip() for a in amenities.split(",") if a.strip()]

    # =========================
    # 🖼 IMAGE UPLOAD (CLOUDINARY 🔥)
    # =========================
    image_urls = []

    try:
        for file in files:
            result = cloudinary.uploader.upload(file)
            image_urls.append(result["secure_url"])
    except Exception as e:
        print("❌ Image Upload Error:", e)
        return jsonify({"success": False, "error": "Image upload failed"}), 500

    # =========================
    # 📍 MAP LOCATION
    # =========================
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    try:
        latitude = float(latitude) if latitude else None
        longitude = float(longitude) if longitude else None
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

        "images": image_urls,  # 🔥 cloud URLs
        "amenities": amenities,

        "latitude": latitude,
        "longitude": longitude,

        "phone": phone,
        "whatsapp": whatsapp,

        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    print("✅ Saving to DB:", house)

    try:
        result = db.houses.insert_one(house)

        return jsonify({
            "success": True,
            "message": "House added successfully ✅",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        print("❌ DB ERROR:", e)
        return jsonify({"success": False, "error": "Database error"}), 500