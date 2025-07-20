from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import config
import re
from data_manager import save_users

# --- Conversation States ---
AWAITING_UPI, AWAITING_AMOUNT = range(2)

# Dictionary to hold withdrawal states
user_withdraw_state = {}

# Withdrawal Options (Coin Needed)
withdraw_options = {
    "100": 2000,
    "300": 6000,
    "500": 10000,
    "1000": 20000
}

# --- Menu Button to Start Withdrawal ---
async def show_withdrawal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("₹100", callback_data="withdraw_100"),
         InlineKeyboardButton("₹300", callback_data="withdraw_300")],
        [InlineKeyboardButton("₹500", callback_data="withdraw_500"),
         InlineKeyboardButton("₹1000", callback_data="withdraw_1000")],
        [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
    ]
    await query.message.edit_text("🔢 Select withdrawal amount:", reply_markup=InlineKeyboardMarkup(keyboard))
    return AWAITING_AMOUNT

# --- Handle Selection (Amount Button) ---
async def process_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    amount = query.data.split("_")[1]
    required_coins = withdraw_options.get(amount)

    if config.USERS[user_id]["coins"] < required_coins:
        await query.message.edit_text("❌ Not enough coins to withdraw this amount.")
        return ConversationHandler.END

    user_withdraw_state[user_id] = {"amount": amount, "required": required_coins}
    await query.message.edit_text("💡 Please send your UPI ID to complete withdrawal.")
    return AWAITING_UPI

# --- Handle UPI ID Input ---
async def get_upi_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    upi = update.message.text.strip()

    if not re.match(r"^[\w.\-]{2,}@[a-zA-Z]{2,}$", upi):
        await update.message.reply_text("❌ Invalid UPI format. Example: `yourname@upi`")
        return AWAITING_UPI

    if user_id not in user_withdraw_state:
        await update.message.reply_text("❌ No active withdrawal session.")
        return ConversationHandler.END

    data = user_withdraw_state.pop(user_id)
    amount = data["amount"]
    required = data["required"]

    config.USERS[user_id]["coins"] -= required

    # Save request
    config.USERS[user_id].setdefault("withdrawals", []).append({
        "amount": amount,
        "upi": upi
    })
    save_users(config.USERS)

    await update.message.reply_text(f"✅ Withdrawal of ₹{amount} requested.\n⏳ Wait 24 hours.")

    # Notify Admin
    try:
        await context.bot.send_message(
            chat_id=config.OWNER_ID,
            text=f"📥 New Withdrawal\n👤 User ID: <code>{user_id}</code>\n💸 ₹{amount}\n🏦 UPI: <code>{upi}</code>",
            parse_mode="HTML"
        )
    except:
        pass

    return ConversationHandler.END

# --- Static fallback (Menu) if called directly ---
async def show_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    coins = config.USERS[user_id]["coins"]

    text = (
        f"💰 Total Coins: {coins} Coin\n"
        f"🧾 2000 Coin = ₹100\n"
        f"🔢 Click below to withdraw:"
    )
    buttons = [
        [InlineKeyboardButton("💳 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
