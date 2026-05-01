from flask import Flask
from flask_cors import CORS
from config import Config
from pymongo import MongoClient

# Import routes
from routes.house_routes import house_bp
from routes.auth_routes import auth_bp
from routes.furniture_routes import furniture_bp   # ✅ NEW

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

print("MONGO_URI:", app.config["MONGO_URI"])

client = MongoClient(app.config["MONGO_URI"])
db = client["rental_db"]

app.db = db

app.config["SECRET_KEY"] = app.config.get("SECRET_KEY", "secret123")

@app.route("/")
def home():
    return {"message": "Backend + MongoDB Connected 🚀"}

# ✅ Register routes
app.register_blueprint(house_bp, url_prefix="/api/houses")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(furniture_bp, url_prefix="/api/furniture")  # ✅ NEW

if __name__ == "__main__":
    app.run(debug=True)