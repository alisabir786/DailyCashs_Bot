from telegram import Update
from telegram.ext import ContextTypes
from task import handle_game_answer
from profile import update_profile_photo
from admin_handler import broadcast_command

# Text Message Handler
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.startswith("/broadcast"):
        await broadcast_command(update, context)
        return

    # Check game answer
    await handle_game_answer(update, context)

# Photo Handler (for profile pic)
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Profile photo updated!")
    update_profile_photo(update)
