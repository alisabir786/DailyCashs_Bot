# withdrawal.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
import config

AWAITING_UPI, AWAITING_AMOUNT = range(2)

# Step 1️⃣: Show Withdraw Menu
async def show_withdrawal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()
    await query.message.reply_text("💵 আপনার UPI ID দিন (যেমন: yourname@upi):")
    return AWAITING_UPI

# Step 2️⃣: UPI Save
async def get_upi_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    upi = update.message.text.strip()
    context.user_data["upi"] = upi

    keyboard = [
        [InlineKeyboardButton("₹100 (2000 coin)", callback_data="withdraw_100")],
        [InlineKeyboardButton("₹300 (6000 coin)", callback_data="withdraw_300")],
        [InlineKeyboardButton("₹500 (10000 coin)", callback_data="withdraw_500")],
        [InlineKeyboardButton("₹1000 (20000 coin)", callback_data="withdraw_1000")]
    ]
    await update.message.reply_text(
        "✅ UPI ID গ্রহণ করা হয়েছে। এখন আপনি উইথড্র অ্যামাউন্ট বেছে নিন:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return AWAITING_AMOUNT

# Step 3️⃣: Handle Amount Selection
async def process_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    coins = config.USERS[user_id]["coins"]

    amount_map = {
        "withdraw_100": (100, 2000),
        "withdraw_300": (300, 6000),
        "withdraw_500": (500, 10000),
        "withdraw_1000": (1000, 20000)
    }

    selected = query.data
    amount, required_coins = amount_map[selected]

    if coins < required_coins:
        await query.answer("❌ আপনার কাছে পর্যাপ্ত কয়েন নেই!", show_alert=True)
        return ConversationHandler.END

    config.USERS[user_id]["coins"] -= required_coins
    upi = context.user_data.get("upi")

    await query.message.edit_text(
        f"✅ আপনার ₹{amount} এর উইথড্রাল অনুরোধ গ্রহণ করা হয়েছে।\n\n"
        f"🧾 UPI: `{upi}`\n"
        f"⏳ অনুগ্রহ করে ২৪ ঘন্টা অপেক্ষা করুন।"
    )

    # Notify Admin (Future improvement: Send to OWNER_ID)
    owner_id = config.OWNER_ID
    try:
        await context.bot.send_message(
            chat_id=owner_id,
            text=(
                f"🔔 নতুন Withdrawal অনুরোধ:\n\n"
                f"👤 ইউজার: {query.from_user.first_name} (@{query.from_user.username})\n"
                f"🆔 ID: {user_id}\n"
                f"💰 Amount: ₹{amount}\n"
                f"💵 UPI: {upi}"
            )
        )
    except:
        pass

    return ConversationHandler.END
    
