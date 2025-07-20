# wallet.py
from telegram import Update
from telegram.ext import ContextTypes
import config

async def show_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    coins = config.USERS.get(user_id, {}).get("coins", 0)

    text = f"💰 আপনার ওয়ালেট ব্যালেন্স:\n\n🔸 কয়েন: {coins} 🪙"

    await query.edit_message_text(text=text)
