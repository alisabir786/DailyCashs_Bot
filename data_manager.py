from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# 🔐 Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# 📦 MongoDB connection
client = MongoClient(MONGO_URI or "mongodb://localhost:27017/")
db = client["dailycashs"]

# Collections
users_col = db["users"]
wallets_col = db["wallets"]
checkin_col = db["checkins"]
spin_col = db["spins"]
task_col = db["tasks"]

# ✅ Add new user
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

# 🔍 Get user
def get_user(user_id):
    return users_col.find_one({"user_id": user_id})

# 📦 Get full user data
def get_user_data(user_id):
    user = users_col.find_one({"user_id": user_id})
    wallet = wallets_col.find_one({"user_id": user_id})
    return {
        "user": user,
        "wallet": wallet
    }

# 💰 Get balance
def get_balance(user_id):
    wallet = wallets_col.find_one({"user_id": user_id})
    return wallet["balance"] if wallet else 0

# 💸 Update balance
def update_balance(user_id, amount):
    wallets_col.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )

# ✏️ Update user data
def update_user_data(user_id, data: dict):
    users_col.update_one({"user_id": user_id}, {"$set": data})

# 📋 Get all user IDs
def get_all_users():
    return [user["user_id"] for user in users_col.find({}, {"user_id": 1})]

# ✅ Daily Check-in Functions
def has_checked_in_today(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    return checkin_col.find_one({"user_id": user_id, "date": today}) is not None

def add_checkin(user_id, day, coins):
    today = datetime.now().strftime("%Y-%m-%d")
    checkin_col.insert_one({
        "user_id": user_id,
        "day": day,
        "coins": coins,
        "date": today,
        "timestamp": datetime.now()
    })
    update_balance(user_id, coins)

def get_checkin_history(user_id):
    return list(checkin_col.find({"user_id": user_id}).sort("timestamp", -1))

# 🎯 Spin Game Log
def log_spin(user_id, result):
    spin_col.insert_one({
        "user_id": user_id,
        "result": result,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now()
    })
    update_balance(user_id, result)

def get_today_spin_count(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    return spin_col.count_documents({"user_id": user_id, "date": today})

# 🧩 Task Log Functions
def log_task(user_id, task_type, reward):
    task_col.insert_one({
        "user_id": user_id,
        "task_type": task_type,  # e.g. "video", "game", "refer"
        "reward": reward,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now()
    })
    update_balance(user_id, reward)

def get_today_task_count(user_id, task_type):
    today = datetime.now().strftime("%Y-%m-%d")
    return task_col.count_documents({
        "user_id": user_id,
        "task_type": task_type,
        "date": today
    })

def get_all_task_logs(user_id):
    return list(task_col.find({"user_id": user_id}).sort("timestamp", -1))
    
