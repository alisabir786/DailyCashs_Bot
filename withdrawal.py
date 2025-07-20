# withdrawal.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
import config

# Dictionary to track withdrawal state
user_withdraw_state = {}

withdraw_options = {
    "100": 2000,
    "300": 6000,
    "500": 10000,
    "1000": 20000
}


async def show_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    coins = config.USERS[user_id]["coins"]

    text = (
        f"💰 <b>Total Coins:</b> {coins} Coin\n"
        "🧾 2000 Coin = ₹100\n\n"
        "🔢 <b>Select amount to withdraw:</b>"
    )

    buttons = [
        [InlineKeyboardButton("₹100", callback_data="withdraw_100"),
         InlineKeyboardButton("₹300", callback_data="withdraw_300")],
        [InlineKeyboardButton("₹500", callback_data="withdraw_500"),
         InlineKeyboardButton("₹1000", callback_data="withdraw_1000")],
        [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
    ]

    await query.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


async def handle_withdrawal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    coins = config.USERS[user_id]["coins"]

    amount = query.data.split("_")[1]
    required_coins = withdraw_options.get(amount)

    if coins < required_coins:
        await query.answer("❌ Not enough coins!", show_alert=True)
        return

    # Ask for UPI ID
    user_withdraw_state[user_id] = {
        "amount": amount,
        "required": required_coins
    }

    await query.message.edit_text(
        f"🧾 <b>Withdraw ₹{amount}</b>\n"
        "💡 Please send your <b>UPI ID</b>:",
        parse_mode="HTML"
    )


async def handle_upi_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if user_id not in user_withdraw_state:
        return

    # Save withdrawal
    amount = user_withdraw_state[user_id]["amount"]
    required = user_withdraw_state[user_id]["required"]
    coins = config.USERS[user_id]["coins"]

    if coins < required:
        await update.message.reply_text("❌ You don't have enough coins.")
        user_withdraw_state.pop(user_id, None)
        return

    config.USERS[user_id]["coins"] -= required

    # Save to withdrawal history (or send to admin manually)
    if "withdrawals" not in config.USERS[user_id]:
        config.USERS[user_id]["withdrawals"] = []

    config.USERS[user_id]["withdrawals"].append({
        "amount": amount,
        "upi": message
    })

    user_withdraw_state.pop(user_id, None)

    await update.message.reply_text(
        f"✅ Withdrawal of ₹{amount} successful!\n⏳ Please wait 24 hours for processing.",
    )
    
