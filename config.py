import os
from dotenv import load_dotenv
from data_manager import load_users

# Load .env file
load_dotenv()

# ✅ Load all variables from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
BOT_USERNAME = os.getenv("BOT_USERNAME")

DAILY_REWARD = list(map(int, os.getenv("DAILY_REWARD").split(",")))
SPIN_REWARDS = list(map(int, os.getenv("SPIN_REWARDS").split(",")))

GAME_REWARD = int(os.getenv("GAME_REWARD"))
VIDEO_REWARD = int(os.getenv("VIDEO_REWARD"))
REFER_REWARD = int(os.getenv("REFER_REWARD"))
REFER_PERCENT = float(os.getenv("REFER_PERCENT"))

MIN_WITHDRAWAL = int(os.getenv("MIN_WITHDRAWAL"))
COIN_TO_TAKA = int(os.getenv("COIN_TO_TAKA"))
WITHDRAW_OPTIONS = list(map(int, os.getenv("WITHDRAW_OPTIONS").split(",")))

# ✅ Load users from file
USERS = load_users()
