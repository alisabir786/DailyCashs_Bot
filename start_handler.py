from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data_manager import get_user, add_user

WELCOME_IMG = "https://telegra.ph/file/9b33f0419d0ea9cc9f7c4.jpg"  # ✅ Telegra.ph image link

# ফাংশন: /start কমান্ড
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # ইউজার না থাকলে add_user দিয়ে যোগ করো
    if not get_user(user.id):
        add_user(user.id, user.first_name)

    # Inline Keyboard: ▶️ Play
    keyboard = [[InlineKeyboardButton("▶️ Play", callback_data="open_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send welcome image with caption
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=WELCOME_IMG,
        caption=(
            f"👋 হ্যালো {user.first_name}!\n\n"
            "🎮 স্বাগতম *DailyCashs Bot*-এ!\n\n"
            "💸 টাস্ক, স্পিন এবং রেফার করে ইনকাম করো!\n"
            "💰 টাকা তুলতে পারবে যখন গোল পূর্ণ হবে!\n\n"
            "👇 শুরু করতে *Play* চাপো!"
        ),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
