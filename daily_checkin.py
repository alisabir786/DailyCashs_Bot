# daily_checkin.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config

# ৭ দিনের রিওয়ার্ড
DAY_REWARDS = [4, 8, 16, 32, 72, 90, 120]

# 🔙 Back to Menu বাটন
BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Back to Menu", callback_data="open_menu")]
])

async def show_daily_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_data = config.USERS.get(user.id)

    if not user_data:
        await context.bot.send_message(chat_id, "❌ ইউজার ডেটা পাওয়া যায়নি!")
        return

    day = user_data.get("daily_day", 0)

    if day >= 7:
        await context.bot.send_message(
            chat_id=chat_id,
            text="✅ আপনি ৭ দিনের চেক-ইন শেষ করেছেন! আগামীকাল আবার শুরু করুন।",
            reply_markup=BACK_BUTTON
        )
        return

    coins = DAY_REWARDS[day]
    user_data["coins"] += coins
    user_data["daily_day"] += 1

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"📅 Day {day+1} Check-in Complete!\n"
            f"🎁 আপনি পেয়েছেন: {coins} কয়েন 🪙\n"
            f"💰 মোট কয়েন: {user_data['coins']} 🪙"
        ),
        reply_markup=BACK_BUTTON
    )
    
