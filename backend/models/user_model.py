<<<<<<< HEAD
from flask import current_app

# ✅ CREATE USER
def create_user(user):
    db = current_app.db
    return db.users.insert_one(user)

# ✅ FIND USER BY EMAIL
def find_user(email):
    db = current_app.db
=======
from flask import current_app

# ✅ CREATE USER
def create_user(user):
    db = current_app.db
    return db.users.insert_one(user)

# ✅ FIND USER BY EMAIL
def find_user(email):
    db = current_app.db
>>>>>>> 3e428f534d42f51947e19a872534a44a62a76dd8
    return db.users.find_one({"email": email})