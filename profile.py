from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import config

AWAITING_NAME, AWAITING_PHOTO = range(2)

# ✅ Show profile
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_data = config.USERS.get(user.id, {})

    name = user_data.get("name", user.first_name)
    coins = user_data.get("coins", 0)

    keyboard = [
        [InlineKeyboardButton("Edit Name", callback_data="edit_name")],
        [InlineKeyboardButton("Edit Photo", callback_data="edit_photo")],
        [InlineKeyboardButton("Privacy", callback_data="privacy"),
         InlineKeyboardButton("About", callback_data="about")],
        [InlineKeyboardButton("Back", callback_data="menu")]
    ]

    await query.answer()
    await query.edit_message_text(
        text=f"👤 *Profile*\n\n🆔 ID: `{user.id}`\n👤 Name: {name}\n🪙 Coins: {coins}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ✅ Ask for name
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("✍️ Enter your new name:")
    return AWAITING_NAME

# ✅ Save name
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    user_id = update.effective_user.id

    config.USERS.setdefault(user_id, {})["name"] = name
    await update.message.reply_text(f"✅ Name updated to *{name}*", parse_mode="Markdown")
    return ConversationHandler.END

# ✅ Ask for photo
async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("📸 Send your new profile photo:")
    return AWAITING_PHOTO

# ✅ Save photo
async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo_file_id = update.message.photo[-1].file_id

    config.USERS.setdefault(user_id, {})["photo"] = photo_file_id
    await update.message.reply_text("✅ Photo updated successfully!")
    return ConversationHandler.END

# ✅ Show Privacy
async def show_privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text="🔒 *Privacy Policy*\n\nWe only store your Telegram ID, name, and game-related data to enhance your experience.\nWe never share your data with third parties.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="profile")]])
    )

# ✅ Show About
async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text="ℹ️ *About DailyCashs*\n\nEarn coins by completing simple tasks and redeem them for real money via UPI.\n\nCreated by @Sabirdigital",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="profile")]])
    )
    
