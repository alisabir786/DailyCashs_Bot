from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data_manager import users_col, wallets_col

WELCOME_IMG = "https://telegra.ph/file/9b33f0419d0ea9cc9f7c4.jpg"  # replace with your image

# ফাংশন: ইউজার একবারে শুরু করলে ( /start )
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # নতুন ইউজার হলে ডেটাবেজে অ্যাড করো
    if not users_col.find_one({"user_id": user.id}):
        users_col.insert_one({
            "user_id": user.id,
            "name": user.first_name,
            "username": user.username,
            "photo": None,
            "joined": update.effective_message.date.isoformat()
        })

        wallets_col.insert_one({
            "user_id": user.id,
            "coins": 0
        })

    # Inline Button: "▶️ Play"
    keyboard = [[InlineKeyboardButton("▶️ Play", callback_data="open_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=WELCOME_IMG,
        caption=(
            "👋 Welcome to *DailyCashs Bot*\n\n"
            "💸 Earn coins by completing tasks, spinning the wheel, and referring friends!\n"
            "💰 Withdraw when you reach the goal.\n\n"
            "👇 Press *Play* to get started!"
        ),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
