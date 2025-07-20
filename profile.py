# profile.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
import config
import os

user_profile_state = {}

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_data = config.USERS.get(user.id, {})

    profile_text = (
        f"👤 <b>Your Profile</b>\n\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"📛 <b>Name:</b> {user_data.get('first_name', '')}\n"
        f"🔰 <b>Username:</b> @{user.username}\n"
        f"💰 <b>Coin:</b> {user_data.get('coins', 0)}\n\n"
        f"🔒 <b>Privacy:</b> All your data is secure.\n"
        f"ℹ️ <b>About:</b> Earn coins by completing daily tasks!"
    )

    buttons = [
        [InlineKeyboardButton("✏️ Change Name", callback_data="change_name")],
        [InlineKeyboardButton("📷 Upload Photo", callback_data="upload_photo")],
        [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
    ]

    await query.message.edit_text(profile_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


# Step 1: Change name
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_profile_state[query.from_user.id] = "change_name"
    await query.message.edit_text("✏️ Please send your new name:")


async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_profile_state.get(user_id) != "change_name":
        return

    new_name = update.message.text
    config.USERS[user_id]["first_name"] = new_name
    user_profile_state.pop(user_id)

    await update.message.reply_text(f"✅ Name updated to: {new_name}")


# Step 2: Upload Photo
async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_profile_state[query.from_user.id] = "upload_photo"
    await query.message.edit_text("📷 Please send your profile photo now:")


async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_profile_state.get(user_id) != "upload_photo":
        return

    if not update.message.photo:
        await update.message.reply_text("❌ Please send a photo only.")
        return

    photo_file = await update.message.photo[-1].get_file()
    file_path = f"assets/profile_{user_id}.jpg"
    await photo_file.download_to_drive(file_path)

    config.USERS[user_id]["profile_photo"] = file_path
    user_profile_state.pop(user_id)

    await update.message.reply_text("✅ Profile photo updated!")


