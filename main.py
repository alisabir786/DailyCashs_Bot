from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from wallet import show_wallet
from profile import show_profile
from daily_checkin import show_daily_checkin
from spin import show_spin
from task import show_task
from withdrawal import show_withdrawal_menu

import config

# 👋 /start command
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
        f"👋 হ্যালো {user.first_name}!\n\n"
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে ইনকাম করুন!\n\n"
        "👇 শুরু করতে Play বাটনে ক্লিক করুন:"
    )

    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/3cnfGR0/welcome-image.png",
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

    data = query.data

    if data == "open_menu":
        await query.edit_message_caption(
            caption="🏠 মেইন মেনু:",
            reply_markup=get_main_menu()
        )
    elif data == "wallet":
        await show_wallet(update, context)
    elif data == "profile":
        await show_profile(update, context)
    elif data == "daily_checkin":
        await show_daily_checkin(update, context)
    elif data == "spin":
        await show_spin(update, context)
    elif data == "task":
        await show_task(update, context)
    elif data == "withdraw":
        await show_withdrawal_menu(update, context)
    elif data == "profile_settings":
        await query.edit_message_text("⚙️ প্রোফাইল সেটিংস লোড হচ্ছে...")

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
    
