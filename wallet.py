import sys
import os
sys.path.append(os.path.dirname(__file__))

from telegram import Update
from telegram.ext import ContextTypes
import config

# ইউজারের কয়েন দেখাও
async def show_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in config.USERS:
        await update.message.reply_text("⚠️ আপনি প্রথমে /start করুন।")
        return

    coins = config.USERS[user_id].get("coins", 0)
    await update.message.reply_text(f"💰 আপনার মোট কয়েন: {coins} 🪙")

# কয়েন যোগ করার ফাংশন (অন্য মডিউলে ব্যবহার হবে)
def add_coins(user_id, amount):
    if user_id in config.USERS:
        config.USERS[user_id]["coins"] += amount
    else:
        config.USERS[user_id] = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "coins": amount,
            "daily_day": 0,
            "referrals": [],
            "profile_photo": None
        }

# কয়েন কমানোর ফাংশন
def deduct_coins(user_id, amount):
    if user_id in config.USERS and config.USERS[user_id]["coins"] >= amount:
        config.USERS[user_id]["coins"] -= amount
        return True
    return False
