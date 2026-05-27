from flask import jsonify
from services.house_scraper import get_tumkur_houses

def fetch_houses():

    data = get_tumkur_houses()

    return jsonify(data)