from flask import Blueprint, request, jsonify
from controllers.furniture_controller import add_furniture, get_furniture

furniture_bp = Blueprint("furniture", __name__)

# ✅ ADD
@furniture_bp.route("/add", methods=["POST"])
def add():
    return jsonify(add_furniture(request.json))

# ✅ GET ALL
@furniture_bp.route("/", methods=["GET"])
def get_all():
    return jsonify(get_furniture())