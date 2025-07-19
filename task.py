from telegram import Update
from telegram.ext import ContextTypes
import config

async def show_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user = config.USERS.get(user_id)

    if not user:
        await query.edit_message_text("❌ ইউজার খুঁজে পাওয়া যায়নি!")
        return

    total_earned = config.GAME_REWARD + config.VIDEO_REWARD
    user["coins"] += total_earned

    await query.edit_message_text(
        f"🧩 গেম এবং ভিডিও টাস্ক কমপ্লিট!\n"
        f"🎮 গেম: {config.GAME_REWARD} কয়েন\n"
        f"🎥 ভিডিও: {config.VIDEO_REWARD} কয়েন\n"
        f"💰 মোট আয়: {total_earned} কয়েন\n"
        f"📦 ব্যালান্স: {user['coins']} কয়েন"
    )
