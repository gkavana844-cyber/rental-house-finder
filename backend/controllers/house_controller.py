from flask import current_app
from datetime import datetime
import re


def add_house(data):
    db = current_app.db

    print("🔥 Incoming Data:", data)

    # =========================
    # ✅ REQUIRED VALIDATION
    # =========================
    title = data.get("title")
    location = data.get("location")

    if not title or not location:
        return {
            "success": False,
            "error": "Title and Location are required"
        }

    # =========================
    # ✅ TYPE
    # =========================
    house_type = data.get("type", "rent")

    if house_type not in ["rent", "lease"]:
        return {"success": False, "error": "Invalid house type"}

    # =========================
    # 💰 PRICE / LEASE
    # =========================
    price = data.get("price")
    lease_duration = data.get("lease_duration")

    if house_type == "rent":
        if not price:
            return {"success": False, "error": "Monthly rent required"}

        try:
            price = int(price)
        except:
            return {"success": False, "error": "Invalid price"}

        lease_duration = None

    elif house_type == "lease":
        if not lease_duration:
            return {"success": False, "error": "Lease duration required"}

        try:
            lease_duration = int(lease_duration)
        except:
            return {"success": False, "error": "Invalid lease duration"}

        price = None

    # =========================
    # 📞 PHONE + WHATSAPP (NEW)
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

    # 🔴 Validate phone
    if not phone or len(phone) != 10:
        return {"success": False, "error": "Invalid phone number"}

    if whatsapp and len(whatsapp) != 10:
        return {"success": False, "error": "Invalid WhatsApp number"}

    # =========================
    # 🧾 AMENITIES
    # =========================
    amenities = data.get("amenities", [])
    if isinstance(amenities, str):
        amenities = [a.strip() for a in amenities.split(",") if a.strip()]

    # =========================
    # 🖼 IMAGES
    # =========================
    images = data.get("images", [])
    if not images and data.get("image"):
        images = [data.get("image")]

    if not isinstance(images, list):
        images = []

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

        "images": images,
        "amenities": amenities,

        "latitude": latitude,
        "longitude": longitude,

        # 🔥 NEW FIELDS
        "phone": phone,
        "whatsapp": whatsapp,

        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    print("✅ Saving to DB:", house)

    try:
        result = db.houses.insert_one(house)

        return {
            "success": True,
            "message": "House added successfully ✅",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        print("❌ DB ERROR:", e)
        return {
            "success": False,
            "error": "Database error"
        }