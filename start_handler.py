from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if user.id not in config.USERS:
        config.USERS[user.id] = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "coins": 0,
            "daily_day": 0,
            "referrals": [],
            "profile_photo": None
        }

    welcome_text = f"👋 হ্যালো {user.first_name}!\n\n🎮 ইনকাম করতে শুরু করুন নিচের Play বাটনে ক্লিক করে!"
    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/3cnfGR0/welcome-image.png",
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
        ])
    )
