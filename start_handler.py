from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from data_manager import db

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    
    # ইউজার চেক করুন
    if not db.get_user(user.id):
        db.create_user(user.id, user.first_name, user.last_name, user.username)
    
    # ওয়েলকাম মেসেজ
    welcome_text = (
        "🎉 স্বাগতম DailyCashs বটে! 🎉\n\n"
        "🎮 গেম খেলে, টাস্ক কমপ্লিট করে, স্পিন হুইল ঘুরিয়ে টাকা ইনকাম করুন!\n"
        "💰 প্রতিদিন ডেইলি রিওয়ার্ড ক্লেইম করুন এবং রেফার করে আরও বেশি আয় করুন!"
    )
    
    # বাটন
    keyboard = [
        [InlineKeyboardButton("▶️ প্লে বাটন", callback_data='play')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ইমেজ সহ মেসেজ সেন্ড
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('assets/banner.jpg', 'rb'),
        caption=welcome_text,
        reply_markup=reply_markup
    )

def setup_start_handler(dp):
    dp.add_handler(CommandHandler("start", start))
