# profile.py

from telegram import Update
from telegram.ext import ContextTypes
import config


async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in config.USERS:
        await update.callback_query.edit_message_text("❌ ইউজার পাওয়া যায়নি।")
        return

    data = config.USERS[user_id]

    profile_text = (
        f"👤 আপনার প্রোফাইল\n\n"
        f"🆔 ইউজার আইডি: `{user_id}`\n"
        f"📛 নাম: {data.get('first_name', 'N/A')} {data.get('last_name', '')}\n"
        f"🔗 ইউজারনেম: @{data.get('username', 'N/A')}\n"
        f"💰 কয়েন: {data.get('coins', 0)} 🪙\n"
    )

    await update.callback_query.edit_message_text(
        profile_text,
        parse_mode="Markdown"
    )
