from flask import Flask
from flask_cors import CORS
from config import Config
from pymongo import MongoClient
import os

# =========================
# ✅ IMPORT ROUTES
# =========================
from routes.house_routes import house_bp
from routes.auth_routes import auth_bp
from routes.furniture_routes import furniture_bp
from routes.nearby_routes import nearby_bp
from routes.external_routes import external_bp

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

    client = MongoClient(mongo_uri)

    db = client["rental_db"]

    app.db = db

    print("✅ MongoDB Connected")

except Exception as e:
    print("❌ MongoDB Connection Error:", e)

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
        "message":
        "Rental House Finder API Running 🚀"
    }

# =========================
# 🔗 REGISTER BLUEPRINTS
# =========================

# Houses
app.register_blueprint(
    house_bp,
    url_prefix="/api/houses"
)

# Authentication
app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

# Furniture
app.register_blueprint(
    furniture_bp,
    url_prefix="/api/furniture"
)

# Nearby Houses
app.register_blueprint(
    nearby_bp,
    url_prefix="/api/nearby"
)

# External Houses API
app.register_blueprint(
    external_bp,
    url_prefix="/api/external"
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