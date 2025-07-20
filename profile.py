import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import config
from data_manager import save_users  # ✅ সঠিকভাবে import

user_profile_state = {}

# 📌 Show Profile
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_data = config.USERS.setdefault(user.id, {"coins": 0})

    profile_text = (
        f"👤 <b>Your Profile</b>\n\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"📛 <b>Name:</b> {user_data.get('first_name', 'Not Set')}\n"
        f"🔰 <b>Username:</b> @{user.username or 'N/A'}\n"
        f"💰 <b>Coin:</b> {user_data.get('coins', 0)}\n\n"
        f"🔒 <b>Privacy:</b> All your data is secure.\n"
        f"ℹ️ <b>About:</b> Earn coins by completing daily tasks!"
    )

    buttons = [
        [InlineKeyboardButton("✏️ Change Name", callback_data="edit_name")],
        [InlineKeyboardButton("📷 Upload Photo", callback_data="edit_photo")],
        [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
    ]

    await query.message.edit_text(
        profile_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✏️ Step 1: Ask for new name
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_profile_state[query.from_user.id] = "change_name"
    await query.message.edit_text("✏️ আপনার নতুন নাম পাঠান:")

# ✅ Save new name
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_profile_state.get(user_id) != "change_name":
        return

    new_name = update.message.text.strip()
    config.USERS.setdefault(user_id, {})["first_name"] = new_name
    save_users(config.USERS)  # ✅ ডেটা ফাইল-এ সেভ করা
    user_profile_state.pop(user_id)

    await update.message.reply_text(f"✅ আপনার নাম আপডেট হয়েছে: {new_name}")

# 📷 Step 2: Ask for photo
async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_profile_state[query.from_user.id] = "upload_photo"
    await query.message.edit_text("📷 দয়া করে এখন আপনার প্রোফাইল ফটো পাঠান:")

# ✅ Save profile photo
async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_profile_state.get(user_id) != "upload_photo":
        return

    if not update.message.photo:
        await update.message.reply_text("❌ দয়া করে শুধুমাত্র একটি ফটো পাঠান।")
        return

    photo_file = await update.message.photo[-1].get_file()
    os.makedirs("assets", exist_ok=True)
    file_path = f"assets/profile_{user_id}.jpg"
    await photo_file.download_to_drive(file_path)

    config.USERS.setdefault(user_id, {})["profile_photo"] = file_path
    save_users(config.USERS)  # ✅ সেভ করে রাখি
    user_profile_state.pop(user_id)

    await update.message.reply_text("✅ আপনার প্রোফাইল ফটো আপডেট হয়েছে!")
    
