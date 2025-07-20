from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from wallet import show_wallet
from profile import show_profile

# মেনু ডিজাইন
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet"),
         InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("📅 Daily Check-in", callback_data="daily_checkin")],
        [InlineKeyboardButton("🎯 Spin", callback_data="spin")],
        [InlineKeyboardButton("🧩 Task", callback_data="task")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="profile_settings")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")]
    ])

# Callback Menu Handler
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "open_menu":
        await query.edit_message_caption(
            caption="🏠 মেইন মেনু:",
            reply_markup=get_main_menu()
        )
# Add in your callback_handler
elif data == "wallet":
    await show_wallet(update, context)
elif data == "profile":
    await show_profile(update, context)
elif data == "daily_checkin":
    await show_daily_checkin(update, context)
