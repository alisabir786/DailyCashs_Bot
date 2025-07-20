from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from start_handler import start
from callback_handler import callback_handler
from telegram.ext import MessageHandler, filters
from task import handle_game_answer

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_game_answer))


def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()

# Add in your callback_handler
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
from withdrawal import show_withdrawal_menu, get_upi_id, process_withdraw, AWAITING_UPI, AWAITING_AMOUNT
from telegram.ext import ConversationHandler, MessageHandler, filters

withdraw_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(show_withdrawal_menu, pattern="^withdraw$")],
    states={
        AWAITING_UPI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_upi_id)],
        AWAITING_AMOUNT: [CallbackQueryHandler(process_withdraw, pattern="^withdraw_")]
    },
    fallbacks=[]
)

app.add_handler(withdraw_conv)

