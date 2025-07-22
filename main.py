import os
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from start_handler import start_command
from callback_handler import callback_handler
from message_handler import message_handler, photo_handler
from profile import ask_new_name, save_new_name, update_profile_photo
from dotenv import load_dotenv

# 🔐 .env থেকে টোকেন লোড করো
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Conversation State for Name Update
NAME_UPDATE = range(1)

def main():
    app = Application.builder().token(TOKEN).build()

    # 🔹 Start command
    app.add_handler(CommandHandler("start", start_command))

    # 🔹 Callback query (button click)
    app.add_handler(CallbackQueryHandler(callback_handler))

    # 🔹 Text message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # 🔹 Photo message handler (Profile photo update)
    app.add_handler(MessageHandler(filters.PHOTO, update_profile_photo))

    # 🔹 Name Update Conversation
    app.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(ask_new_name, pattern="update_name")],
        states={
            NAME_UPDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_new_name)],
        },
        fallbacks=[],
    ))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
