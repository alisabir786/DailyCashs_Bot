from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # ইউজার নতুন হলে config.USERS ডিকশনারিতে এন্ট্রি তৈরি করো
    if user.id not in config.USERS:
        config.USERS[user.id] = {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username or "",
            "coins": 0,
            "daily_day": 0,
            "referrals": [],
            "profile_photo": None
        }

    # ওয়েলকাম টেক্সট
    welcome_text = (
        f"👋 হ্যালো {user.first_name}!\n\n"
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে ইনকাম করুন!\n\n"
        "👇 শুরু করতে Play বাটনে ক্লিক করুন:"
    )

    # ইমেজ সহ মেসেজ পাঠানো (imgur লিংক ব্যবহার করা হয়েছে, এটা ঠিকঠাক কাজ করে)
    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.imgur.com/yXKp4Lw.png",  # Telegram-compatible ইমেজ লিংক
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
        ])
    )

