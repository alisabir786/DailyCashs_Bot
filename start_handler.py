from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from referral import add_referral


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

    # নতুন ইউজার রেজিস্ট্রেশন
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

        # রেফারেল সংযুক্তি
        if referrer_id and referrer_id != user.id:
            if referrer_id in config.USERS:
                if user.id not in config.USERS[referrer_id]["referrals"]:
                    config.USERS[referrer_id]["referrals"].append(user.id)
                    config.USERS[referrer_id]["coins"] += config.REFER_REWARD
                    config.USERS[referrer_id]["ref_bonus"] = config.USERS[referrer_id].get("ref_bonus", 0) + config.REFER_REWARD

    # Welcome মেসেজ
    welcome_text = (
        f"👋 হ্যালো {user.first_name or 'বন্ধু'}!\n\n"
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে ইনকাম করুন!\n\n"
        "👇 শুরু করতে নিচের Play বাটনে ক্লিক করুন:"
    )

    # ইমেজ সহ মেসেজ পাঠানো
    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/q3RkVXLB/welcome.png",  # ✅ তুমি দেওয়া ওয়েলকাম ব্যানার
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
        ])
    )
    
