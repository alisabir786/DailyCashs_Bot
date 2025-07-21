from telegram import Update
from telegram.ext import ContextTypes
from data_manager import get_user_data

async def show_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # ইউজারের ডেটা আনো
    user_data = get_user_data(user_id)
    balance = user_data.get("wallet", 0)
    total_earned = user_data.get("total_earned", 0)

    text = (
        f"💼 *Your Wallet*\n\n"
        f"💰 Current Balance: `{balance}` coins\n"
        f"📈 Total Earned: `{total_earned}` coins\n\n"
        f"🔁 Coins will be added automatically when you complete tasks, check-ins, or spin the wheel."
    )

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )
