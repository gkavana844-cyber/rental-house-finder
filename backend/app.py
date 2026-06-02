from flask import Flask
from flask_cors import CORS
from config import Config
from pymongo import MongoClient
from mongoengine import connect
import os

# =========================
# ✅ IMPORT ROUTES
# =========================
from routes.house_routes import house_bp
from routes.auth_routes import auth_bp
from routes.furniture_routes import furniture_bp
from routes.activityRoutes import activity_routes

# =========================
# 🚀 APP INIT
# =========================
app = Flask(__name__)

app.config.from_object(Config)

# =========================
# 🌐 CORS
# =========================
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

# =========================
# 🧠 MONGODB CONNECTION
# =========================
try:

    mongo_uri = (
        os.environ.get("MONGO_URI")
        or app.config.get("MONGO_URI")
    )

    if not mongo_uri:
        raise Exception("MONGO_URI not found")

    print("MONGO_URI Loaded")

    # =========================
    # PyMongo Connection
    # =========================
    client = MongoClient(mongo_uri)

    db = client["rental_db"]

    app.db = db

    print("✅ PyMongo Connected")

    # =========================
    # MongoEngine Connection
    # =========================
    connect(
        db="rental_db",
        host=mongo_uri
    )

    print("✅ MongoEngine Connected")

except Exception as e:

    print(
        "❌ MongoDB Connection Error:",
        str(e)
    )

# =========================
# 🔐 SECRET KEY
# =========================
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "secret123"
)

# =========================
# 🏠 HOME ROUTE
# =========================
@app.route("/")
def home():

    return {
        "success": True,
        "message": "Rental House Finder API Running 🚀"
    }

# =========================
# 📊 DASHBOARD STATS
# =========================
@app.route("/api/dashboard/stats")
def dashboard_stats():

    try:

        total_users = app.db.users.count_documents({})
        total_houses = app.db.houses.count_documents({})
        total_searches = app.db.searches.count_documents({})

        pipeline = [
            {
                "$group": {
                    "_id": "$location",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            },
            {
                "$limit": 1
            }
        ]

        result = list(
            app.db.searches.aggregate(
                pipeline
            )
        )

        top_location = (
            result[0]["_id"]
            if result
            else "No Data"
        )

        return {
            "success": True,
            "data": {
                "total_users": total_users,
                "total_houses": total_houses,
                "total_searches": total_searches,
                "top_location": top_location
            }
        }, 200

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }, 500

# =========================
# 🔗 REGISTER BLUEPRINTS
# =========================

app.register_blueprint(
    house_bp,
    url_prefix="/api/houses"
)

app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

app.register_blueprint(
    furniture_bp,
    url_prefix="/api/furniture"
)

# ✅ Activity Routes
app.register_blueprint(
    activity_routes
)

# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )