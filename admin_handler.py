from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import config

# Admin Panel Command
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != config.OWNER_ID:
        await update.message.reply_text("❌ আপনি এই কমান্ড ব্যবহারের অনুমতি রাখেন না।")
        return

    await update.message.reply_text(
        "🛠️ Welcome to Admin Panel",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Withdraw Requests", callback_data="admin_withdraw_list")],
            [InlineKeyboardButton("👥 All Users", callback_data="admin_users")],
        ])
    )

# Approve / Reject Withdraw Requests
pending_withdraws = {}

async def list_withdraw_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text_lines = []

    for uid, user in config.USERS.items():
        if "withdraw_request" in user:
            w = user["withdraw_request"]
            text_lines.append(
                f"🧾 User: {uid}\nAmount: {w['amount']}\nCoin: {w['coin']}\nUPI: {w['upi']}"
            )
            pending_withdraws[str(uid)] = w

    if not text_lines:
        await query.edit_message_text("✅ কোনো pending withdraw নেই।")
        return

    message = "\n\n".join(text_lines)
    buttons = [[
        InlineKeyboardButton("✅ Approve", callback_data="admin_approve"),
        InlineKeyboardButton("❌ Reject", callback_data="admin_reject")
    ]]
    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(buttons))

# Approve Withdraw
async def approve_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    for uid in pending_withdraws:
        user = config.USERS[int(uid)]
        w = user["withdraw_request"]

        del user["withdraw_request"]
        await context.bot.send_message(
            chat_id=uid,
            text=f"✅ আপনার উইথড্র ({w['amount']}) সফলভাবে approve হয়েছে!\nআপনার অ্যাকাউন্টে টাকা ২৪ ঘণ্টার মধ্যে পাঠানো হবে।"
        )

    await query.edit_message_text("🎉 সব withdraw সফলভাবে approve করা হয়েছে।")
    pending_withdraws.clear()

# Reject Withdraw
async def reject_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    for uid in pending_withdraws:
        user = config.USERS[int(uid)]
        w = user["withdraw_request"]

        del user["withdraw_request"]
        user["coins"] += w["coin"]

        await context.bot.send_message(
            chat_id=uid,
            text=f"❌ আপনার উইথড্র ({w['amount']}) বাতিল করা হয়েছে।\nCoin ফেরত দেওয়া হলো।"
        )

    await query.edit_message_text("🚫 সব withdraw বাতিল করা হয়েছে।")
    pending_withdraws.clear()
