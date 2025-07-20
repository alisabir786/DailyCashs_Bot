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

    welcome_text = (
        f"👋 হ্যালো {user.first_name or 'বন্ধু'}!\n\n"
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে ইনকাম করুন!\n\n"
        "👇 শুরু করতে নিচের Play বাটনে ক্লিক করুন:"
    )

    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/3cnfGR0/welcome-image.png",  # ভবিষ্যতে assets ফোল্ডারে আপলোড করতে পারো
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
        ])
    )
from referral import add_referral

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # নতুন ইউজার রেজিস্টার
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

        # রেফার সিস্টেম
        if context.args:
            referrer_id = int(context.args[0])
            add_referral(user.id, referrer_id)

    # বাকি Welcome মেসেজ আগের মতোই থাকবে
    
# Add in start_handler.py > start function

referrer_id = None

# Handle /start <referral_id>
if context.args:
    try:
        referrer_id = int(context.args[0])
        if referrer_id != user.id and user.id not in config.USERS[referrer_id]["referrals"]:
            config.USERS[referrer_id]["referrals"].append(user.id)
            config.USERS[referrer_id]["coins"] += 10  # instant bonus
            config.USERS[referrer_id]["ref_bonus"] = config.USERS[referrer_id].get("ref_bonus", 0) + 10
    except:
        pass
        
