from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # রেফারার আইডি খুঁজে বের করা (যদি থাকে)
    referrer_id = None
    if context.args:
        try:
            referrer_id = int(context.args[0])
        except:
            referrer_id = None

    # ইউজার নতুন কিনা চেক
    if user.id not in config.USERS:
        config.USERS[user.id] = {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "username": user.username or "",
            "coins": 0,
            "daily_day": 0,
            "referrals": [],
            "ref_bonus": 0,
            "profile_photo": None
        }

        # রেফারেল যুক্তি (নিজেকে রেফার করতে না পারে)
        if referrer_id and referrer_id != user.id and referrer_id in config.USERS:
            if user.id not in config.USERS[referrer_id]["referrals"]:
                config.USERS[referrer_id]["referrals"].append(user.id)
                config.USERS[referrer_id]["coins"] += config.REFER_REWARD
                config.USERS[referrer_id]["ref_bonus"] += config.REFER_REWARD

    # Welcome টেক্সট
    welcome_text = (
        f"👋 হ্যালো {user.first_name or 'বন্ধু'}!\n\n"
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে ইনকাম করুন!\n\n"
        "👇 শুরু করতে নিচের Play বাটনে ক্লিক করুন:"
    )

    # ইমেজ সহ মেসেজ পাঠানো
    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/q3RkVXLB/welcome.png",  # ✅ ওয়েলকাম ব্যানার
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
        ])
    )
    
