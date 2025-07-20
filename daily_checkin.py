from telegram import Update
from telegram.ext import ContextTypes
import config
from data_manager import save_users  # ✅ যুক্ত করেছি

async def show_daily_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = config.USERS.setdefault(user_id, {
        "coins": 0,
        "daily_day": 0
    })

    # Ensure daily_day is within valid range
    day = user_data.get("daily_day", 0)

    if day >= 7:
        await query.edit_message_text("✅ আপনি এই সপ্তাহে সব চেক-ইন সম্পন্ন করেছেন!\n\nআগামী সপ্তাহে আবার চেক-ইন শুরু হবে।")
        return

    # Get reward from config
    reward = config.DAILY_REWARD[day]

    # ✅ Update user's coin and day
    user_data["coins"] += reward
    user_data["daily_day"] = day + 1

    save_users(config.USERS)  # ✅ এখানেই সেভ করে ফেললাম

    # Prepare check-in status list
    checkmarks = ["✅" if i < user_data["daily_day"] else "🔓" for i in range(7)]

    # Prepare message
    text = (
        "📅 <b>ডেইলি চেক-ইন:</b>\n\n"
        f"১ম দিন - 4 🪙 {checkmarks[0]}\n"
        f"২য় দিন - 8 🪙 {checkmarks[1]}\n"
        f"৩য় দিন - 16 🪙 {checkmarks[2]}\n"
        f"৪র্থ দিন - 32 🪙 {checkmarks[3]}\n"
        f"৫ম দিন - 72 🪙 {checkmarks[4]}\n"
        f"৬ষ্ঠ দিন - 90 🪙 {checkmarks[5]}\n"
        f"৭ম দিন - 120 🪙 {checkmarks[6]}\n\n"
        f"🎉 আজ আপনি পেয়েছেন <b>{reward}</b> কয়েন!"
    )

    await query.edit_message_text(text=text, parse_mode="HTML")
    
