# main.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from wallet import show_wallet         # 💰 Wallet ফাংশন
from profile import show_profile       # 👤 Profile ফাংশন
from daily_checkin import show_daily_checkin  # 📅 Daily Check-in ফাংশন

import config


# 👋 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # ইউজার যদি নতুন হয়
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
        f"👋 হ্যালো {user.first_name}!\n\n"
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে ইনকাম করুন!\n\n"
        "👇 শুরু করতে Play বাটনে ক্লিক করুন:"
    )

    # Welcome Image + Play Button
    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/3cnfGR0/welcome-image.png",  # ইমেজ ইউআরএল বদলাতে পারো
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
        ])
    )


# 🎮 Main Menu
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet"),
         InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("📅 Daily Check-in", callback_data="daily_checkin")],
        [InlineKeyboardButton("🎯 Spin", callback_data="spin")],
        [InlineKeyboardButton("🧩 Task", callback_data="task")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="profile_settings")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")]
    ]
    return InlineKeyboardMarkup(keyboard)


# 📲 Callback Menu Handler
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "open_menu":
        await query.edit_message_caption(
            caption="🏠 মেইন মেনু:",
            reply_markup=get_main_menu()
        )

    elif query.data == "wallet":
        await show_wallet(update, context)

    elif query.data == "profile":
        await show_profile(update, context)

    elif query.data == "daily_checkin":
        await show_daily_checkin(update, context)

    elif query.data == "spin":
        await query.edit_message_text("🎯 স্পিন গেম লোড হচ্ছে...")

    elif query.data == "task":
        await query.edit_message_text("🧩 টাস্ক লোড হচ্ছে...")

    elif query.data == "profile_settings":
        await query.edit_message_text("⚙️ প্রোফাইল সেটিংস লোড হচ্ছে...")

    elif query.data == "withdraw":
        await query.edit_message_text("💵 উইথড্র লোড হচ্ছে...")


# ✅ Bot Start Function
def run_bot():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Bot is running...")
    app.run_polling()


# 🔥 Entry Point
if __name__ == "__main__":
    run_bot()
    
