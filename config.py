from dotenv import load_dotenv
import os

load_dotenv()

# --- Bot Config ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "6955653010"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "@DailyCashs_Bot")

# --- User Data Store ---
USERS = {}

# --- Rewards & Logic ---
DAILY_REWARD = list(map(int, os.getenv("DAILY_REWARD", "10,15,20,25,30,35,50").split(",")))
SPIN_REWARDS = list(map(int, os.getenv("SPIN_REWARDS", "0,5,10,15,20,25,30,50,75,100").split(",")))
GAME_REWARD = int(os.getenv("GAME_REWARD", "10"))
VIDEO_REWARD = int(os.getenv("VIDEO_REWARD", "5"))
REFER_REWARD = int(os.getenv("REFER_REWARD", "10"))
REFER_PERCENT = float(os.getenv("REFER_PERCENT", "0.1"))  # 10%

# --- Withdrawal ---
MIN_WITHDRAWAL = int(os.getenv("MIN_WITHDRAWAL", "2000"))
COIN_TO_TAKA = int(os.getenv("COIN_TO_TAKA", "20"))  # 20 coins = 1৳
WITHDRAW_OPTIONS = list(map(int, os.getenv("WITHDRAW_OPTIONS", "2000,4000,6000").split(",")))

# Optional: Convert rate in INR
COINS_PER_1_INR = 20  # 2000 coin = ₹100
