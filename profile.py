# profile.py
from telegram import Update
from telegram.ext import ContextTypes
import config

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = config.USERS.get(user.id, {})

    text = (
        f"👤 প্রোফাইল তথ্য:\n\n"
        f"🆔 ইউজার ID: {user.id}\n"
        f"📛 নাম: {data.get('first_name', '')} {data.get('last_name', '')}\n"
        f"🔰 ইউজারনেম: @{data.get('username', 'N/A')}\n"
        f"💰 কয়েন: {data.get('coins', 0)} 🪙"
    )

    await query.edit_message_text(text=text)
