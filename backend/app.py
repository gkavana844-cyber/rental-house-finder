from flask import Flask
from flask_cors import CORS
from config import Config
from mongoengine import connect
from pymongo import MongoClient
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
CORS(app, resources={r"/*": {"origins": "*"}})

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

    print("MONGO_URI:", mongo_uri)

    # ✅ PyMongo connection (for existing code)
    client = MongoClient(mongo_uri)
    db = client["rental_db"]
    app.db = db

    # ✅ MongoEngine connection (for Activity model)
    connect(
        'rental_db',
        host=mongo_uri,
        alias='default'
    )

    print("✅ MongoDB Connected")
    print("✅ MongoEngine Connected")

except Exception as e:
    print("❌ MongoDB Connection Error:", e)

# =========================
# 🔐 SECRET KEY
# =========================
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY"
)

# =========================
# 🏠 HOME ROUTE
# =========================
@app.route("/")
def home():
    return {
        "message": "Rental House Finder API Running 🚀"
    }

# =========================
# 📊 ADMIN DASHBOARD STATS ROUTE
# =========================
@app.route("/api/dashboard/stats")
def dashboard_stats():
    """Get dashboard statistics"""
    try:
        from services.activityService import ActivityService
        stats = ActivityService.get_dashboard_stats()
        return {
            'success': True,
            'data': stats
        }, 200
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }, 500

# =========================
# 🔗 REGISTER BLUEPRINTS
# =========================

# Houses API
app.register_blueprint(
    house_bp,
    url_prefix="/api/houses"
)

# Authentication API
app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

# Furniture API
app.register_blueprint(
    furniture_bp,
    url_prefix="/api/furniture"
)

# ✅ Activity API (NEW)
app.register_blueprint(
    activity_routes,
    url_prefix="/api/activities"
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