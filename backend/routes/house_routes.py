from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
import json
import re
import cloudinary
import cloudinary.uploader
import os
from services.activityService import ActivityService

# =========================
# ✅ BLUEPRINT
# =========================
house_bp = Blueprint("house", __name__)

# =========================
# ☁️ CLOUDINARY CONFIG
# =========================
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("CLOUD_API_KEY"),
    api_secret=os.environ.get("CLOUD_API_SECRET"),
    secure=True
)

# =========================
# 📞 CLEAN PHONE NUMBER
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

        # FORM DATA
        data = request.form

        # =========================
        # 🪑 FURNITURE DATA
        # =========================
        print("🔥 FURNITURE RAW:", data.get("furniture"))

        try:
            furniture = json.loads(
                data.get("furniture", "[]")
            )
            print("🔥 FURNITURE PARSED:", furniture)
        except Exception as e:
            print("🔥 FURNITURE ERROR:", e)
            furniture = []

        # FILES
        files = request.files.getlist("images")

        print("🔥 FORM DATA:", data)
        print("🔥 FILES:", files)

        title = data.get("title")
        location = data.get("location")

        if not title:
            return jsonify({
                "success": False,
                "error": "Title required"
            }), 400

        if not location:
            return jsonify({
                "success": False,
                "error": "Location required"
            }), 400

        # HOUSE TYPE
        house_type = data.get(
            "type",
            "rent"
        )

        # PRICE
        price = data.get("price")

        # LEASE
        lease_duration = data.get(
            "lease_duration"
        )

        # RENT TYPE
        if house_type == "rent":

            if not price:
                return jsonify({
                    "success": False,
                    "error": "Price required"
                }), 400

            price = int(price)

            lease_duration = None

        # LEASE TYPE
        elif house_type == "lease":

            if not lease_duration:
                return jsonify({
                    "success": False,
                    "error":
                    "Lease duration required"
                }), 400

            lease_duration = int(
                lease_duration
            )

            price = None

        # PHONE
        phone = clean_number(
            data.get("phone")
        )

        whatsapp = clean_number(
            data.get("whatsapp")
        )

        if not phone or len(phone) != 10:

            return jsonify({
                "success": False,
                "error":
                "Invalid phone number"
            }), 400

        if whatsapp and len(whatsapp) != 10:

            return jsonify({
                "success": False,
                "error":
                "Invalid WhatsApp number"
            }), 400

        # AMENITIES
        amenities = data.get(
            "amenities",
            ""
        )

        amenities = [
            a.strip()
            for a in amenities.split(",")
            if a.strip()
        ]

        # =========================
        # ☁️ CLOUDINARY IMAGE UPLOAD
        # =========================
        image_urls = []

        for file in files:

            if file and file.filename != "":

                try:

                    result = cloudinary.uploader.upload(
                        file
                    )

                    print(
                        "☁️ CLOUDINARY:",
                        result
                    )

                    image_urls.append(
                        result["secure_url"]
                    )

                except Exception as upload_error:

                    print(
                        "❌ IMAGE ERROR:",
                        upload_error
                    )

        # LOCATION COORDINATES
        latitude = (
            float(data.get("latitude"))
            if data.get("latitude")
            else None
        )

        longitude = (
            float(data.get("longitude"))
            if data.get("longitude")
            else None
        )

        # HOUSE OBJECT
        house = {

            "title": title,

            "location":
            location.strip(),

            "type": house_type,

            "price": price,

            "lease_duration":
            lease_duration,

            "images": image_urls,

            "amenities": amenities,

            "latitude": latitude,

            "longitude": longitude,

            "phone": phone,

            "whatsapp": whatsapp,

            # 🪑 SAVE FURNITURE
            "furniture": furniture,

            "created_at":
            datetime.utcnow(),

            "updated_at":
            datetime.utcnow()
        }

        # SAVE TO DB
        result = db.houses.insert_one(
            house
        )

        # =========================
        # ✅ LOG ACTIVITY
        # =========================
        try:
            ActivityService.log_activity(
                activity_type="house_added",
                description=f"House added in {location}",
                user_id=phone,
                metadata={
                    "house_id": str(result.inserted_id),
                    "title": title,
                    "location": location,
                    "type": house_type
                }
            )
        except Exception as log_error:
            print("⚠️ Activity Log Error:", log_error)

        return jsonify({

            "success": True,

            "message":
            "House added successfully ✅",

            "id":
            str(result.inserted_id)

        }), 201

    except Exception as e:

        print("❌ ADD HOUSE ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# ✅ GET ALL HOUSES
# =========================
@house_bp.route("/", methods=["GET"])
def get_houses():

    db = current_app.db

    houses = list(
        db.houses.find().sort(
            "created_at",
            -1
        )
    )

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

        house = db.houses.find_one({
            "_id": ObjectId(id)
        })

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