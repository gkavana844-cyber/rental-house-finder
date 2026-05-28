import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    CLOUD_NAME = os.getenv("CLOUD_NAME")

    CLOUD_API_KEY = os.getenv(
        "CLOUD_API_KEY"
    )

    CLOUD_API_SECRET = os.getenv(
        "CLOUD_API_SECRET"
    )