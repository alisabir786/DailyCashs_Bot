from telegram import Update
from telegram.ext import ContextTypes
import random, config

async def show_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user = config.USERS.get(user_id)

    if not user:
        await query.edit_message_text("❌ ইউজার খুঁজে পাওয়া যায়নি!")
        return

    reward = random.choice(config.SPIN_REWARDS)
    user["coins"] += reward

    await query.edit_message_text(
        f"🎯 আপনি স্পিনে পেয়েছেন: {reward} কয়েন!\n"
        f"💰 মোট কয়েন: {user['coins']}"
    )
