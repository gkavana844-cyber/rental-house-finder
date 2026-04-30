from flask import current_app

# ✅ CREATE USER
def create_user(user):
    db = current_app.db
    return db.users.insert_one(user)

# ✅ FIND USER BY EMAIL
def find_user(email):
    db = current_app.db
    return db.users.find_one({"email": email})