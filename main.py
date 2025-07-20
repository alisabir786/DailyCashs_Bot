from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from start_handler import start
from callback_handler import callback_handler

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
