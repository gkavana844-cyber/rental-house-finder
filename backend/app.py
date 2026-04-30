from flask import Flask
from flask_cors import CORS
from config import Config
from pymongo import MongoClient

# Import routes
from routes.house_routes import house_bp
from routes.auth_routes import auth_bp   # 🔥 NEW

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

# Debug
print("MONGO_URI:", app.config["MONGO_URI"])

# MongoDB Connection
client = MongoClient(app.config["MONGO_URI"])
db = client["rental_db"]

app.db = db

# ✅ SECRET KEY (for JWT)
app.config["SECRET_KEY"] = app.config.get("SECRET_KEY", "secret123")

# Home route
@app.route("/")
def home():
    return {"message": "Backend + MongoDB Connected 🚀"}

# ✅ Register Blueprints
app.register_blueprint(house_bp, url_prefix="/api/houses")
app.register_blueprint(auth_bp, url_prefix="/api/auth")  # 🔥 NEW

# Run server
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)