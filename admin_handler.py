from telegram import Update
from telegram.ext import ContextTypes
from data_manager import get_all_users

ADMIN_ID = 6955653010  # আপনার Telegram User ID

# Broadcast Command Handler
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔️ You are not authorized.")
        return

    msg = update.message.text.split(" ", 1)
    if len(msg) != 2:
        await update.message.reply_text("❗Usage:\n/broadcast Your message here")
        return

    text = msg[1]
    users = get_all_users()
    success = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 *Admin Message:*\n{text}", parse_mode="Markdown")
            success += 1
        except:
            continue

    await update.message.reply_text(f"✅ Broadcast sent to {success} users.")
