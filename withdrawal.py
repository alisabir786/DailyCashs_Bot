from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config

# ✅ Withdrawal states
AWAITING_UPI, AWAITING_AMOUNT = range(2)

# ✅ Show Withdrawal Menu
async def show_withdrawal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("₹100 = 2000 Coins", callback_data="withdraw_10")],
        [InlineKeyboardButton("₹200 = 4000 Coins", callback_data="withdraw_20")],
        [InlineKeyboardButton("₹300 = 6000 Coins", callback_data="withdraw_30")],
        [InlineKeyboardButton("Back", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("💸 Select withdrawal amount:", reply_markup=reply_markup)
    return AWAITING_AMOUNT

# ✅ Handle withdrawal amount selection
async def handle_withdrawal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if not data.startswith("withdraw_"):
        await query.answer("❌ Invalid selection.")
        return

    amount = int(data.split("_")[1])
    coins_required = int((amount / config.COIN_TO_TAKA) * config.MIN_WITHDRAWAL)

    user_data = config.USERS.get(user_id, {"coins": 0})
    coins = user_data.get("coins", 0)

    if coins < coins_required:
        await query.edit_message_text(
            text=f"❌ You need {coins_required} coins to withdraw ₹{amount}.\nYour balance: {coins} coins."
        )
        return

    context.user_data["withdraw_amount"] = amount
    await query.edit_message_text("💳 Please enter your UPI ID to proceed:")
    return AWAITING_UPI

# ✅ Get UPI ID from user
async def get_upi_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    upi_id = update.message.text.strip()

    if "@" not in upi_id:
        await update.message.reply_text("❌ Invalid UPI ID. Please enter again:")
        return AWAITING_UPI

    context.user_data["upi_id"] = upi_id
    amount = context.user_data.get("withdraw_amount")

    coins_required = int((amount / config.COIN_TO_TAKA) * config.MIN_WITHDRAWAL)
    user_data = config.USERS.get(user_id, {"coins": 0})

    if user_data["coins"] < coins_required:
        await update.message.reply_text("❌ Insufficient coins.")
        return ConversationHandler.END

    # Deduct coins and record
    user_data["coins"] -= coins_required
    user_data.setdefault("withdrawals", []).append({
        "amount": amount,
        "upi_id": upi_id
    })
    config.USERS[user_id] = user_data

    await update.message.reply_text(
        f"✅ Withdrawal request for ₹{amount} received!\nUPI: `{upi_id}`\n\n⏳ It will be processed soon.",
        parse_mode="Markdown"
    )

    # Notify Admin
    owner_id = int(config.OWNER_ID)
    try:
        await context.bot.send_message(
            chat_id=owner_id,
            text=f"💰 New Withdrawal Request\n\nUser: [{update.effective_user.first_name}](tg://user?id={user_id})\nAmount: ₹{amount}\nUPI: `{upi_id}`\nBalance Left: {user_data['coins']} coins",
            parse_mode="Markdown"
        )
    except:
        pass

    return ConversationHandler.END

# ✅ Show current withdrawal info
async def show_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = config.USERS.get(user_id, {"coins": 0})

    coins = user_data.get("coins", 0)
    taka = coins // config.COIN_TO_TAKA
    can_withdraw = "✅ Yes" if coins >= config.MIN_WITHDRAWAL else "❌ Not Yet"

    await query.answer()
    await query.edit_message_text(
        text=(
            f"💰 Withdrawal Info:\n\n"
            f"Coins: {coins} 🪙\n"
            f"Estimated ₹: {taka}\n"
            f"Eligible for Withdrawal: {can_withdraw}\n\n"
            f"➡️ Minimum {config.MIN_WITHDRAWAL} coins required for withdrawal.\n"
            f"Select 'Withdraw' to proceed."
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Withdraw Now", callback_data="withdraw")],
            [InlineKeyboardButton("Back", callback_data="menu")]
        ])
    )

# ✅ Handle UPI fallback
async def handle_upi_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "@" in text:
        return await get_upi_id(update, context)
    else:
        return await handle_text(update, context)  # From message_handler
