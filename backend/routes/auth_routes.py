from flask import Blueprint, request, jsonify
from controllers.auth_controller import register_user, login_user

auth_bp = Blueprint("auth", __name__)


# =========================
# ✅ REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid or missing JSON data"
        }), 400

    result = register_user(data)

    # 🔥 Status handling
    if result.get("success"):
        return jsonify(result), 201
    else:
        return jsonify(result), 400


# =========================
# ✅ LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid or missing JSON data"
        }), 400

    result = login_user(data)

    # 🔥 Status handling
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 401