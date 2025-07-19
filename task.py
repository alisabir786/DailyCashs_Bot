from telegram import Update
from telegram.ext import ContextTypes
import config

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (
        "🧩 আজকের টাস্ক:\n\n"
        f"🎮 গেম খেলে আয়: +{config.GAME_REWARD} কয়েন\n"
        f"🎥 ভিডিও দেখলে আয়: +{config.VIDEO_REWARD} কয়েন\n"
        "\n(ডেমো বট: কোন রিয়েল গেম/ভিডিও নেই)"
    )
    await context.bot.send_message(chat_id, text)
