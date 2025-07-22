from pymongo import MongoClient
from config import Config
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client.dailycashs_bot
        
    def get_user(self, user_id):
        return self.db.users.find_one({"user_id": user_id})
    
    def create_user(self, user_id, first_name, last_name, username):
        user_data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "balance": 0,
            "streak": 0,
            "last_streak_date": None,
            "referral_code": f"REF{user_id}",
            "referred_by": None,
            "referrals": [],
            "created_at": datetime.now()
        }
        self.db.users.insert_one(user_data)
    
    def update_balance(self, user_id, amount):
        self.db.users.update_one(
            {"user_id": user_id},
            {"$inc": {"balance": amount}}
        )
    
    # অন্যান্য ডেটাবেস মেথড...
    
db = Database()
