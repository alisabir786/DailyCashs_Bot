# message_handler.py
from telegram import Update
from telegram.ext import ContextTypes
import config

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if context.user_data.get("awaiting_upi"):
        context.user_data["awaiting_upi"] = False

        upi = text
        coin_amount = context.user_data.get("withdraw_coin")
        money = context.user_data.get("withdraw_amount")

        # Validate user data exists
        user_data = config.USERS.setdefault(user_id, {"coins": 0})

        if user_data.get("coins", 0) < coin_amount:
            await update.message.reply_text("❌ আপনার অ্যাকাউন্টে যথেষ্ট কয়েন নেই!")
            return

        # Deduct coins & save withdrawal info
        user_data["coins"] -= coin_amount
        user_data["withdraw_request"] = {
            "coin": coin_amount,
            "amount": money,
            "upi": upi
        }

        # Admin Notification
        log = (
            f"🧾 <b>[Withdraw Request]</b>\n"
            f"👤 User ID: <code>{user_id}</code>\n"
            f"💰 Coin: <b>{coin_amount}</b>\n"
            f"💵 Amount: ₹{money}\n"
            f"🏦 UPI: <code>{upi}</code>"
        )

        await context.bot.send_message(
            chat_id=config.OWNER_ID,
            text=log,
            parse_mode="HTML"
        )

        # Confirmation to user
        await update.message.reply_text(
            f"✅ আপনার উইথড্র রিকোয়েস্ট গ্রহণ করা হয়েছে!\n💵 টাকা: ₹{money}\n📅 ২৪ ঘণ্টার মধ্যে আপনার UPI-তে পাঠানো হবে।"
        )
