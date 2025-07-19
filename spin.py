from telegram import Update
from telegram.ext import ContextTypes
import random
import config

async def play_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_data = config.USERS.get(user.id)

    if not user_data:
        await context.bot.send_message(chat_id, "❌ ইউজার ডেটা পাওয়া যায়নি!")
        return

    reward = random.choice(config.SPIN_REWARDS)
    user_data["coins"] += reward

    await context.bot.send_message(
        chat_id,
        f"🎯 আপনি স্পিন করে পেয়েছেন: {reward} কয়েন!\n💰 মোট কয়েন: {user_data['coins']}"
    )
