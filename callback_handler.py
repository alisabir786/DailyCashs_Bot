from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Import feature handlers
from wallet import show_wallet
from profile import show_profile, ask_name, ask_photo
from daily_checkin import show_daily_checkin
from spin import show_spin, do_spin
from task import show_task, game_task, video_task, refer_task
from referral import show_referral
from withdrawal import show_withdrawal

# 🔘 Main menu layout
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet"),
         InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("📅 Daily Check-in", callback_data="daily_checkin")],
        [InlineKeyboardButton("🎯 Spin", callback_data="spin")],
        [InlineKeyboardButton("🧩 Task", callback_data="task")],
        [InlineKeyboardButton("👥 Refer & Earn", callback_data="referral")],
        [InlineKeyboardButton("💸 Withdrawal", callback_data="withdrawal")]
    ])

# 📲 Callback menu handler
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # 🏠 Back to Main Menu
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

    elif data == "do_spin":
        await do_spin(update, context)

    elif data == "task":
        await show_task(update, context)

    elif data == "game_task":
        await game_task(update, context)

    elif data == "video_task":
        await video_task(update, context)

    elif data == "refer_task":
        await refer_task(update, context)

    elif data == "referral":
        await show_referral(update, context)

    elif data == "withdrawal":
        await show_withdrawal(update, context)

    # ✅ Profile Edit Options
    elif data == "edit_name":
        await ask_name(update, context)

    elif data == "edit_photo":
        await ask_photo(update, context)

    else:
        await query.edit_message_text("❌ অজানা কমান্ড!")
        
