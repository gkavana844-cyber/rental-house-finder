from flask import Flask
from flask_cors import CORS
from config import Config
from pymongo import MongoClient
import os

# Import routes
from routes.house_routes import house_bp
from routes.auth_routes import auth_bp
from routes.furniture_routes import furniture_bp

# =========================
# 🚀 APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# =========================
# 🌐 CORS (ALLOW FRONTEND)
# =========================
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# 🧠 MONGODB CONNECTION
# =========================
try:
    mongo_uri = app.config["MONGO_URI"]
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
app.config["SECRET_KEY"] = app.config.get("SECRET_KEY", "secret123")

# =========================
# 🏠 HOME ROUTE
# =========================
@app.route("/")
def home():
    return {"message": "Backend + MongoDB Connected 🚀"}

# =========================
# 🔗 REGISTER ROUTES
# =========================
app.register_blueprint(house_bp, url_prefix="/api/houses")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(furniture_bp, url_prefix="/api/furniture")

# =========================
# 🚀 RUN SERVER (RAILWAY FIX)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔥 IMPORTANT
    app.run(host="0.0.0.0", port=port)