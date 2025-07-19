import os
from dotenv import load_dotenv

load_dotenv()  # .env ফাইল থেকে ভেরিয়েবল লোড

# 🔐 Secure Configurations from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
BOT_USERNAME = os.getenv("BOT_USERNAME")

# 🎁 Daily Check-in Rewards
DAILY_REWARD = [4, 8, 16, 32, 72, 90, 120]

# 🎯 Spin Rewards
SPIN_REWARDS = [0, 5, 10, 30, 50, 100]

# 🧩 Task Rewards
GAME_REWARD = 5
VIDEO_REWARD = 5

# 👥 Referral
REFER_REWARD = 10
REFER_PERCENT = 0.10

# 💵 Withdraw Settings
MIN_WITHDRAWAL = 2000
COIN_TO_TAKA = 100
WITHDRAW_OPTIONS = [100, 300, 500, 1000]

# 🗃️ In-Memory Dummy Database
USERS = {}
