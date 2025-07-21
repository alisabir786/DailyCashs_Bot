from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from wallet import show_wallet
from profile import show_profile
from daily_checkin import handle_checkin
from spin import start_spin
from task import show_tasks
from withdrawal import process_withdraw

# Callback function for all buttons
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Home menu button
    if data == "open_menu":
        keyboard = [
            [InlineKeyboardButton("💰 Wallet", callback_data="wallet"),
             InlineKeyboardButton("👤 Profile", callback_data="profile")],
            [InlineKeyboardButton("🎁 Daily Check-in", callback_data="daily_checkin")],
            [InlineKeyboardButton("🎯 Spin", callback_data="spin")],
            [InlineKeyboardButton("🧠 Tasks", callback_data="tasks")],
            [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="🏠 *Main Menu* — Choose an option below:",
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif data == "wallet":
        await show_wallet(update, context)

    elif data == "profile":
        await show_profile(update, context)

    elif data == "daily_checkin":
        await handle_checkin(update, context)

    elif data == "spin":
        await start_spin(update, context)

    elif data == "tasks":
        await show_tasks(update, context)

    elif data == "withdraw":
        await process_withdraw(update, context)

    else:
        await query.edit_message_text("❌ Unknown option selected.")
        
