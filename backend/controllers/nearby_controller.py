from flask import current_app, request, jsonify
from services.location_service import calculate_distance

def get_nearby_houses():

    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))

    houses = list(
        current_app.db.houses.find({})
    )

    results=[]

    for house in houses:

        if "latitude" not in house:
            continue

        distance=calculate_distance(
            lat,
            lng,
            house["latitude"],
            house["longitude"]
        )

        if distance <= 10:

            house["_id"]=str(house["_id"])
            house["distance"]=round(distance,2)

            results.append(house)

    results.sort(
        key=lambda x:x["distance"]
    )

    return jsonify(results)