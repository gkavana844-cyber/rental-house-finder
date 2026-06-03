from flask import Blueprint, request, jsonify
import os
import jwt
import datetime

admin_bp = Blueprint("admin", __name__)

# =========================
# 🔐 ADMIN LOGIN
# =========================
@admin_bp.route("/login", methods=["POST"])
def admin_login():

    try:
        data = request.get_json()

        password = data.get("password")

        admin_password = os.getenv("ADMIN_PASSWORD")

        if not password:
            return jsonify({
                "success": False,
                "error": "Password required"
            }), 400

        if password != admin_password:
            return jsonify({
                "success": False,
                "error": "Invalid Admin Password"
            }), 401

        token = jwt.encode(
            {
                "role": "admin",
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(hours=12)
            },
            os.getenv("SECRET_KEY", "secret123"),
            algorithm="HS256"
        )

        return jsonify({
            "success": True,
            "message": "Admin Login Successful",
            "token": token
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500