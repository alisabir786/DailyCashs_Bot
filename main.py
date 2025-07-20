from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters
)
from config import BOT_TOKEN

# Handlers
from start_handler import start
from callback_handler import callback_handler
from task import handle_game_answer
from withdrawal import (
    show_withdrawal_menu, get_upi_id, process_withdraw,
    AWAITING_UPI, AWAITING_AMOUNT,
    show_withdrawal, handle_withdrawal_selection, handle_upi_input
)
from profile import (
    show_profile, ask_name, save_name,
    ask_photo, save_photo,
    show_privacy, show_about,
    AWAITING_NAME, AWAITING_PHOTO
)
from referral import show_referral
from message_handler import handle_text
from admin_handler import admin_panel

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 🔹 Start and Callback
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    # 🔹 Game Task Answer
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_game_answer))

    # 🔹 Withdrawal Conversation
    withdraw_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(show_withdrawal_menu, pattern="^withdraw$")],
        states={
            AWAITING_UPI: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_upi_id)],
            AWAITING_AMOUNT: [CallbackQueryHandler(process_withdraw, pattern="^withdraw_")]
        },
        fallbacks=[]
    )
    app.add_handler(withdraw_conv)

    # 🔹 Profile Conversation
    profile_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(ask_name, pattern="^edit_name$"),
            CallbackQueryHandler(ask_photo, pattern="^edit_photo$")
        ],
        states={
            AWAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)],
            AWAITING_PHOTO: [MessageHandler(filters.PHOTO, save_photo)]
        },
        fallbacks=[]
    )
    app.add_handler(profile_conv)

    # 🔹 Static Callback Buttons
    app.add_handler(CallbackQueryHandler(show_profile, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(show_privacy, pattern="^privacy$"))
    app.add_handler(CallbackQueryHandler(show_about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(show_referral, pattern="^referral$"))
    app.add_handler(CallbackQueryHandler(show_withdrawal, pattern="^withdrawal$"))
    app.add_handler(CallbackQueryHandler(handle_withdrawal_selection, pattern="^withdraw_"))

    # 🔹 Fallback message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_upi_input))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, save_photo))

    # 🔹 Admin
    app.add_handler(CommandHandler("panel", admin_panel))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
    
