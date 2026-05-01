from flask import Blueprint, request, jsonify
from controllers.furniture_controller import add_furniture, get_furniture

furniture_bp = Blueprint("furniture", __name__)

# ✅ ADD (UPDATED FOR IMAGE UPLOAD)
@furniture_bp.route("/add", methods=["POST"])
def add():
    result = add_furniture()  # 🔥 no request.json
    return jsonify(result)


# ✅ GET ALL
@furniture_bp.route("/", methods=["GET"])
def get_all():
    result = get_furniture()
    return jsonify(result)