from flask import Flask
from flask_cors import CORS
from config import Config
from pymongo import MongoClient
import os

# =========================
# 🚀 APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# =========================
# 🌐 CORS (ALLOW FRONTEND)
# =========================
CORS(app)

# =========================
# 🧠 MONGODB CONNECTION
# =========================
try:
    mongo_uri = os.environ.get("MONGO_URI") or app.config.get("MONGO_URI")

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
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret123")

# =========================
# 🏠 HOME ROUTE
# =========================
@app.route("/")
def home():
    return {"message": "Backend + MongoDB Connected 🚀"}

# =========================
# 🔗 REGISTER ROUTES
# =========================
from routes.house_routes import house_bp
from routes.auth_routes import auth_bp
from routes.furniture_routes import furniture_bp

app.register_blueprint(house_bp, url_prefix="/api/houses")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(furniture_bp, url_prefix="/api/furniture")

# =========================
# 🚀 RUN SERVER (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)