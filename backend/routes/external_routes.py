from flask import Blueprint
from controllers.external_house_controller import fetch_houses

external_bp = Blueprint(
    "external",
    __name__
)

external_bp.route(
    "/houses",
    methods=["GET"]
)(fetch_houses)