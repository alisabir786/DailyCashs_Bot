import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    MONGO_URI = os.getenv("MONGO_URI")
    COIN_RATE = int(os.getenv("COIN_RATE"))
    
    # Spin wheel rewards
    SPIN_REWARDS = [0, 1, 2, 3, 4, 5, 10, 30, 50, 80, 100]
    SPIN_WEIGHTS = [15, 10, 10, 10, 10, 30, 5, 4, 3, 2, 1]
    
    # Daily streak rewards
    STREAK_REWARDS = {
        1: 4, 2: 8, 3: 16, 
        4: 32, 5: 72, 6: 90, 7: 120
    }
    
    # Task rewards
    GAME_REWARD = 5
    VIDEO_REWARD = 5
    REFERRAL_REWARD = 10
