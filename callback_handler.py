from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from data_manager import db
from config import Config
import random

def handle_callbacks(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    if data == 'play':
        show_home(update, context)
    elif data == 'spin_wheel':
        spin_wheel(update, context)
    # অন্যান্য কলব্যাক হ্যান্ডলিং...

def show_home(update: Update, context: CallbackContext):
    user = update.effective_user
    user_data = db.get_user(user.id)
    
    home_text = (
        f"🏠 আপনার ড্যাশবোর্ড\n\n"
        f"💰 ব্যালেন্স: {user_data['balance']} কয়েন\n"
        f"🔥 স্ট্রিক: {user_data['streak']} দিন"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎡 স্পিন হুইল", callback_data='spin_wheel')],
        [InlineKeyboardButton("📅 ডেইলি চেক-ইন", callback_data='daily_check')],
        [
            InlineKeyboardButton("💼 টাস্ক", callback_data='tasks'),
            InlineKeyboardButton("👤 প্রোফাইল", callback_data='profile'),
            InlineKeyboardButton("💳 উইথড্র", callback_data='withdrawal')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_caption(
        caption=home_text,
        reply_markup=reply_markup
    )

def spin_wheel(update: Update, context: CallbackContext):
    user = update.effective_user
    reward = random.choices(Config.SPIN_REWARDS, weights=Config.SPIN_WEIGHTS, k=1)[0]
    
    db.update_balance(user.id, reward)
    
    result_text = (
        f"🎉 স্পিন রেজাল্ট!\n\n"
        f"🎡 হুইল থেমেছে: {reward} কয়েনে!\n"
        f"💰 আপনার ব্যালেন্স: {db.get_user(user.id)['balance']} কয়েন"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 আবার স্পিন করুন", callback_data='spin_wheel')],
        [InlineKeyboardButton("🏠 হোমে ফিরুন", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=open('assets/wheel.png', 'rb'),
        caption=result_text,
        reply_markup=reply_markup
    )

def setup_callback_handlers(dp):
    dp.add_handler(CallbackQueryHandler(handle_callbacks))
