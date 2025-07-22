from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["dailycashs"]

users_col = db["users"]
wallets_col = db["wallets"]

# ইউজার অ্যাড করো
def add_user(user_id, name, username=None, ref_by=None):
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({
            "user_id": user_id,
            "name": name,
            "username": username,
            "ref_by": ref_by,
            "joined": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "level": "Basic",
            "profile_pic_url": None
        })
        wallets_col.insert_one({"user_id": user_id, "balance": 0})

# ইউজার খোঁজো
def get_user(user_id):
    return users_col.find_one({"user_id": user_id})

# সম্পূর্ণ ইউজার ডেটা আনো
def get_user_data(user_id):
    user = users_col.find_one({"user_id": user_id})
    wallet = wallets_col.find_one({"user_id": user_id})
    return {
        "user": user,
        "wallet": wallet
    }

# ব্যালেন্স আনো
def get_balance(user_id):
    wallet = wallets_col.find_one({"user_id": user_id})
    return wallet["balance"] if wallet else 0

# ব্যালেন্স আপডেট করো
def update_balance(user_id, amount):
    wallets_col.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )

# ইউজার ডেটা আপডেট করো
def update_user_data(user_id, data: dict):
    users_col.update_one({"user_id": user_id}, {"$set": data})

# সব ইউজার আইডি আনো
def get_all_users():
    return [user["user_id"] for user in users_col.find({}, {"user_id": 1})]
    
