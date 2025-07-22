from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from data_manager import get_user_data, update_user_data

# ⬇️ Step 1: Show Profile
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    user_data = get_user_data(user.id)
    username = user.username or "Not Set"
    full_name = user_data.get("custom_name") or f"{user.first_name or ''} {user.last_name or ''}".strip()

    # প্রোফাইল মেসেজ বানাও
    text = (
        f"👤 *User Profile*\n\n"
        f"🆔 ID: `{user.id}`\n"
        f"📛 Name: `{full_name}`\n"
        f"🔰 Username: @{username}\n"
        f"🏆 Level: {user_data.get('level', 'Basic')}\n"
        f"📅 Joined: {user_data.get('joined', 'N/A')}\n\n"
        f"✏️ You can update your *Name* and *Image*. ID and Username can't be changed."
    )

    keyboard = [
        [InlineKeyboardButton("🖼 Update Photo", callback_data="update_photo")],
        [InlineKeyboardButton("✏️ Update Name", callback_data="update_name")],
        [InlineKeyboardButton("🔙 Back to Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    profile_pic = user_data.get("profile_pic_url")
    if profile_pic:
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=profile_pic,
            caption=text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# ⬇️ Step 2: Update Profile Photo
async def update_profile_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)

    if not update.message.photo:
        await update.message.reply_text("❌ কোনো ছবি পাইনি! অনুগ্রহ করে একটি ছবি পাঠাও।")
        return

    photo_file_id = update.message.photo[-1].file_id
    user_data["profile_pic_url"] = photo_file_id
    update_user_data(user_id, user_data)

    await update.message.reply_text("✅ প্রোফাইল ফটো সফলভাবে আপডেট হয়েছে!")

# ⬇️ Step 3: Update Name (Text)
NAME_UPDATE = range(1)

async def ask_new_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text("✏️ আপনার নতুন নাম লিখুন:")
    return NAME_UPDATE

async def save_new_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.text.strip()

    user_data = get_user_data(user_id)
    user_data["custom_name"] = name
    update_user_data(user_id, user_data)

    await update.message.reply_text(f"✅ নাম আপডেট হয়েছে: *{name}*", parse_mode="Markdown")
    return ConversationHandler.END
    
