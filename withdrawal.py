from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import config

async def show_withdrawal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    buttons = [
        [InlineKeyboardButton(f"{amount}৳", callback_data=f"withdraw_{amount}")]
        for amount in config.WITHDRAW_OPTIONS
    ]

    await query.edit_message_text(
        text="💵 কত টাকা উইথড্র করতে চান?",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
