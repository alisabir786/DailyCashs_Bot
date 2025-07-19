from telegram import Update
from telegram.ext import ContextTypes
import config

async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = config.USERS.get(user.id)

    if not user_data:
        return await update.message.reply_text("❌ ইউজার ডেটা পাওয়া যায়নি!")

    refer_link = f"https://t.me/{config.BOT_USERNAME}?start={user.id}"
    await update.message.reply_text(
        f"🔗 আপনার রেফারেল লিংক:\n{refer_link}\n\n"
        f"👥 রেফার সংখ্যা: {len(user_data['referrals'])}\n"
        f"🎁 প্রতি রেফারে ইনকাম: {config.REFER_REWARD} কয়েন"
    )
