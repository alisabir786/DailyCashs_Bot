from telegram import Update
from telegram.ext import ContextTypes
from start_handler import start_menu
from wallet import show_wallet
from profile import show_profile
from daily_checkin import daily_checkin
from spin import spin_wheel
from task import watch_video, play_game
from referral import show_referral

# Callback Button Handler
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "home":
        await start_menu(update, context)
    elif data == "wallet":
        await show_wallet(update, context)
    elif data == "profile":
        await show_profile(update, context)
    elif data == "checkin":
        await daily_checkin(update, context)
    elif data == "spin":
        await spin_wheel(update, context)
    elif data == "watch_video":
        await watch_video(update, context)
    elif data == "game_task":
        await play_game(update, context)
    elif data == "referral":
        await show_referral(update, context)
    else:
        await query.answer("❓ Unknown command")
