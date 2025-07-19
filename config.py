# config.py

BOT_TOKEN = "7577689328:AAFCR1sewFUYRkmm2zNUKACjeOTQa1ZiC3o"  # তোমার Bot Token
OWNER_ID = 6955653010  # Owner/Admin User ID
BOT_USERNAME = "@DailyCashs_Bot"  # Bot Username

# Coins system
DAILY_REWARD = [4, 8, 16, 32, 72, 90, 120]  # 1st to 7th day
SPIN_REWARDS = [0, 5, 10, 30, 50, 100]
GAME_REWARD = 5
VIDEO_REWARD = 5
REFER_REWARD = 10
REFER_PERCENT = 0.10

# Withdrawal config
MIN_WITHDRAWAL = 2000  # coin
COIN_TO_TAKA = 100  # 2000 coin = 100 taka

# Database (we will use in-memory dict for now)
USERS = {}
