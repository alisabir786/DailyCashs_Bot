from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["dailycashs_bot"]

users_col = db["users"]
wallets_col = db["wallets"]
spin_col = db["spins"]
ref_col = db["referrals"]
task_col = db["tasks"]
withdraw_col = db["withdrawals"]
