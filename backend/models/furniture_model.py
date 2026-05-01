from datetime import datetime
import re


def clean_phone(number):
    if not number:
        return None

    digits = re.sub(r"\D", "", number)

    # remove +91 if exists
    if digits.startswith("91"):
        digits = digits[2:]

    # validate 10 digits
    if len(digits) != 10:
        return None

    return digits


def create_furniture(data):
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

    contact = clean_phone(contact)

    # =========================
    # ✅ FINAL OBJECT
    # =========================
    furniture = {
        "name": name.strip(),
        "price": price,
        "contact": contact,
        "created_at": datetime.utcnow()
    }

    return {"success": True, "data": furniture}