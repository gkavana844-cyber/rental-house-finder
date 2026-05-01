from datetime import datetime
import re


# =========================
# 📞 CLEAN PHONE
# =========================
def clean_phone(number):
    if not number:
        return None

    digits = re.sub(r"\D", "", number)

    # remove country code 91
    if digits.startswith("91"):
        digits = digits[2:]

    # validate 10 digits
    if len(digits) != 10:
        return None

    return digits


# =========================
# 🪑 CREATE FURNITURE MODEL
# =========================
def create_furniture(data, image_url=None):
    """
    Validate and prepare furniture data
    """

    name = data.get("name")
    price = data.get("price")
    contact = data.get("contact")

    # =========================
    # ✅ VALIDATION
    # =========================
    if not name:
        return {"success": False, "error": "Furniture name required"}

    if not price:
        return {"success": False, "error": "Price required"}

    try:
        price = int(price)
    except:
        return {"success": False, "error": "Invalid price"}

    # 📞 Clean phone
    contact = clean_phone(contact)

    if not contact:
        return {"success": False, "error": "Invalid phone number"}

    # =========================
    # ✅ FINAL OBJECT
    # =========================
    furniture = {
        "name": name.strip(),
        "price": price,
        "contact": contact,
        "image": image_url,  # 🔥 NEW (optional)
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    return {
        "success": True,
        "data": furniture
    }