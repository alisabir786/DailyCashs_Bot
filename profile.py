from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data_manager import get_user_data

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    user_data = get_user_data(user.id)
    username = user.username or "Not Set"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

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

    # Edit Profile বাটন
    keyboard = [
        [InlineKeyboardButton("🖼 Update Photo", callback_data="update_photo")],
        [InlineKeyboardButton("✏️ Update Name", callback_data="update_name")],
        [InlineKeyboardButton("🔙 Back to Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ছবি সহ প্রোফাইল পাঠাও
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
        
