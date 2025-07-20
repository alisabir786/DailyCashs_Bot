# daily_checkin.py
from telegram import Update
from telegram.ext import ContextTypes
import config

async def show_daily_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = config.USERS.get(user_id, {})
    day = user_data.get("daily_day", 0)

    if day >= 7:
        await query.edit_message_text("✅ আপনি এই সপ্তাহে সব চেক-ইন সম্পন্ন করেছেন!")
        return

    reward = config.DAILY_REWARD[day]
    user_data["coins"] += reward
    user_data["daily_day"] += 1

    checkmarks = ["✅" if i < user_data["daily_day"] else "🔓" for i in range(7)]

    text = (
        "📅 ডেইলি চেক-ইন:\n\n"
        f"১ম দিন - 4 🪙 {checkmarks[0]}\n"
        f"২য় দিন - 8 🪙 {checkmarks[1]}\n"
        f"৩য় দিন - 16 🪙 {checkmarks[2]}\n"
        f"৪র্থ দিন - 32 🪙 {checkmarks[3]}\n"
        f"৫ম দিন - 72 🪙 {checkmarks[4]}\n"
        f"৬ষ্ঠ দিন - 90 🪙 {checkmarks[5]}\n"
        f"৭ম দিন - 120 🪙 {checkmarks[6]}\n\n"
        f"🎉 আজ আপনি পেয়েছেন {reward} কয়েন!"
    )

    await query.edit_message_text(text=text)
    
