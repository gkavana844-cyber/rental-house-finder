<<<<<<< HEAD
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
=======
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
>>>>>>> 3e428f534d42f51947e19a872534a44a62a76dd8
    MONGO_URI = os.getenv("MONGO_URI")