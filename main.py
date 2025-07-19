# main.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import config

# Welcome Keyboard
def get_welcome_keyboard():
    keyboard = [
        [InlineKeyboardButton("▶️ Play", callback_data="open_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Menu Keyboard
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet"),
         InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("📅 Daily Check-in", callback_data="daily_checkin")],
        [InlineKeyboardButton("🎯 Spin", callback_data="spin")],
        [InlineKeyboardButton("📝 Tasks", callback_data="tasks")],
        [InlineKeyboardButton("⚙️ Profile Settings", callback_data="profile_settings")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # ইউজার যদি নতুন হয়, ইউজার যুক্ত করো
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
        "🎮 গেম খেলে, স্পিন করে, টাস্ক কমপ্লিট করে টাকা ইনকাম করুন!\n"
        "👇 নিচের Play বাটনে ক্লিক করুন শুরু করার জন্য:"
    )
    await context.bot.send_photo(
        chat_id=chat_id,
        photo="https://i.ibb.co/3cnfGR0/welcome-image.png",  # একটা ওয়েলকাম ইমেজ URL (তুমি চাইলে কাস্টম দিতে পারো)
        caption=welcome_text,
        reply_markup=get_welcome_keyboard()
    )

# Callback handler
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "open_menu":
        await query.edit_message_caption(
            caption="🏠 মেইন মেনু খুলেছে, নিচ থেকে অপশন বেছে নিন:",
            reply_markup=get_main_menu()
        )
    elif query.data == "wallet":
        await query.edit_message_text("🪙 ওয়ালেট সিস্টেম লোড হচ্ছে...")
    elif query.data == "profile":
        await query.edit_message_text("👤 প্রোফাইল লোড হচ্ছে...")
    elif query.data == "daily_checkin":
        await query.edit_message_text("📅 ডেইলি চেকইন লোড হচ্ছে...")
    elif query.data == "spin":
        await query.edit_message_text("🎯 স্পিন সিস্টেম লোড হচ্ছে...")
    elif query.data == "tasks":
        await query.edit_message_text("📝 টাস্ক লোড হচ্ছে...")
    elif query.data == "profile_settings":
        await query.edit_message_text("⚙️ প্রোফাইল সেটিংস লোড হচ্ছে...")
    elif query.data == "withdraw":
        await query.edit_message_text("💵 উইথড্র সিস্টেম লোড হচ্ছে...")

# Bot রান করানো
def run_bot():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Bot is running...")
    app.run_polling()

# Main entry
if __name__ == "__main__":
    run_bot()
  
