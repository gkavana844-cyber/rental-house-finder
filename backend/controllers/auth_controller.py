import bcrypt
import jwt
import datetime
import re
import os
from models.user_model import create_user, find_user

# 🔐 SECRET from .env
SECRET = os.getenv("SECRET_KEY")


# =========================
# 🔍 VALIDATORS
# =========================

def is_valid_email_or_phone(value):
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^(\+91[\-\s]?)?[6-9]\d{9}$"

    return re.match(email_pattern, value) or re.match(phone_pattern, value)


def is_strong_password(password):
    return (
        len(password) >= 6
        and re.search(r"[A-Z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )


def clean_phone(value):
    digits = re.sub(r"\D", "", value)

    if digits.startswith("91"):
        digits = digits[2:]

    return digits


# =========================
# ✅ REGISTER
# =========================
def register_user(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {"success": False, "error": "All fields required"}

    # 🔴 Validate email/phone
    if not is_valid_email_or_phone(email):
        return {
            "success": False,
            "error": "Enter valid email or Indian phone (+91XXXXXXXXXX)"
        }

    # 🔴 Validate password
    if not is_strong_password(password):
        return {
            "success": False,
            "error": "Password must be 6+ chars with uppercase, number & special char"
        }

    # 🔴 Clean phone if phone used
    if re.match(r"^(\+91[\-\s]?)?[6-9]\d{9}$", email):
        email = clean_phone(email)

    # 🔴 Check existing
    if find_user(email):
        return {"success": False, "error": "User already exists"}

    # 🔐 Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = {
        "name": name,
        "email": email,
        "password": hashed
    }

    create_user(user)

    return {"success": True, "message": "User registered successfully ✅"}


# =========================
# ✅ LOGIN
# =========================
def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"success": False, "error": "Email and password required"}

    # 🔴 Clean phone login
    if re.match(r"^(\+91[\-\s]?)?[6-9]\d{9}$", email):
        email = clean_phone(email)

    user = find_user(email)

    if not user:
        return {"success": False, "error": "User not found"}

    if not bcrypt.checkpw(password.encode(), user["password"]):
        return {"success": False, "error": "Invalid password"}

    # 🔐 JWT token
    token = jwt.encode(
        {
            "user": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        SECRET,
        algorithm="HS256"
    )

    return {"success": True, "token": token}