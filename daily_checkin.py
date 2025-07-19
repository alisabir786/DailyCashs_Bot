# daily_checkin.py

from telegram import Update
from telegram.ext import ContextTypes
import config

DAY_REWARDS = [4, 8, 16, 32, 72, 90, 120]  # সাত দিনের রিওয়ার্ড লিস্ট

async def show_daily_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_data = config.USERS.get(user.id)

    if not user_data:
        await context.bot.send_message(chat_id, "❌ ইউজার ডেটা পাওয়া যায়নি!")
        return

    day = user_data["daily_day"]
    
    if day >= 7:
        await context.bot.send_message(chat_id, "✅ আপনি আজকের চেক-ইন শেষ করেছেন! কাল আবার চেক-ইন করুন।")
        return

    coins = DAY_REWARDS[day]
    user_data["coins"] += coins
    user_data["daily_day"] += 1

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"📅 Day {day+1} Check-in Complete!\n"
            f"🎁 আপনি পেয়েছেন: {coins} কয়েন\n"
            f"💰 আপনার মোট কয়েন: {user_data['coins']}"
        )
    )
