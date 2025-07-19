from telegram import Update
from telegram.ext import ContextTypes
from wallet import show_wallet
from profile import show_profile
from daily_checkin import show_daily_checkin
from spin import play_spin
from task import show_tasks
from withdrawal import handle_withdrawal

from telegram import InlineKeyboardMarkup

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "wallet":
        await show_wallet(update, context)
    elif query.data == "profile":
        await show_profile(update, context)
    elif query.data == "daily_checkin":
        await show_daily_checkin(update, context)
    elif query.data == "spin":
        await play_spin(update, context)
    elif query.data == "task":
        await show_tasks(update, context)
    elif query.data == "withdraw":
        await handle_withdrawal(update, context)
    else:
        await query.edit_message_text("❌ এই অপশনটি এখনও কাজ করে না।")
