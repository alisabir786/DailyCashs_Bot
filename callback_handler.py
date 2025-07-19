from telegram import Update
from telegram.ext import ContextTypes
from wallet import show_wallet
from profile import show_profile
from spin import show_spin
from task import show_task
from withdrawal import show_withdrawal_menu
from daily_checkin import show_daily_checkin

def get_main_menu():
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton

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
    else:
        await query.edit_message_text("⚠️ ফিচারটি এখনো তৈরি হয়নি!")
        
