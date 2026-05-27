from flask import Blueprint
from controllers.nearby_controller import get_nearby_houses

nearby_bp = Blueprint(
    "nearby",
    __name__
)

nearby_bp.route(
    "/",
    methods=["GET"]
)(get_nearby_houses)