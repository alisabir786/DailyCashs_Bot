from telegram import Update
from telegram.ext import ContextTypes
import config

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if context.user_data.get("awaiting_upi"):
        context.user_data["awaiting_upi"] = False

        upi = text
        coin_amount = context.user_data.get("withdraw_coin")
        money = context.user_data.get("withdraw_amount")

        config.USERS[user_id]["coins"] -= coin_amount

        log = f"🧾 [Withdraw Request]\nUser: {user_id}\nCoin: {coin_amount}\nAmount: {money}\nUPI: {upi}"

        # Send to Admin
        await context.bot.send_message(chat_id=config.OWNER_ID, text=log)

        # User confirmation
        await update.message.reply_text(
            f"✅ আপনার উইথড্র রিকোয়েস্ট গ্রহণ করা হয়েছে।\n💰 Amount: {money}\n📅 পেমেন্ট ২৪ ঘণ্টার মধ্যে পাঠানো হবে।"
        )
