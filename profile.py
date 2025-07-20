# profile.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

import config

AWAITING_NAME, AWAITING_PHOTO = range(2)

# Step 1️⃣: Show Profile Info
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_data = config.USERS[user.id]

    profile_text = (
        f"👤 <b>প্রোফাইল</b>\n\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
        f"📛 <b>Name:</b> {user_data.get('first_name', 'N/A')}\n"
        f"💰 <b>Coins:</b> {user_data.get('coins', 0)}\n"
    )

    buttons = [
        [InlineKeyboardButton("✏️ Edit Name", callback_data="edit_name")],
        [InlineKeyboardButton("🖼️ Edit Photo", callback_data="edit_photo")],
        [InlineKeyboardButton("🔐 Privacy Policy", callback_data="privacy")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
    ]

    await query.message.edit_text(
        profile_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Step 2️⃣: Edit Name
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()
    await query.message.reply_text("✏️ নতুন নাম লিখুন:")
    return AWAITING_NAME

async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    config.USERS[update.effective_user.id]["first_name"] = name
    await update.message.reply_text("✅ নাম সফলভাবে আপডেট হয়েছে।")
    return ConversationHandler.END

# Step 3️⃣: Edit Photo
async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()
    await query.message.reply_text("📸 একটি ছবি পাঠান (Profile Photo হিসেবে ব্যবহার হবে):")
    return AWAITING_PHOTO

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = f"profile_pics/{user_id}.jpg"
    await file.download_to_drive(file_path)

    config.USERS[user_id]["profile_photo"] = file_path
    await update.message.reply_text("✅ প্রোফাইল ছবি আপডেট হয়েছে।")
    return ConversationHandler.END

# Step 4️⃣: Privacy & About
async def show_privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(
        "🔐 <b>Privacy Policy</b>\n\nআপনার তথ্য শুধুমাত্র অ্যাপ ব্যবহারের জন্য রাখা হয়। অন্য কারো সাথে শেয়ার করা হয় না।",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="profile")]])
    )

async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(
        "ℹ️ <b>About</b>\n\nএই অ্যাপটি গেম, ভিডিও, স্পিন ও টাস্ক সম্পূর্ণ করে আয় করার জন্য তৈরি। Made by @Sabirdigital",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="profile")]])
    )
    
