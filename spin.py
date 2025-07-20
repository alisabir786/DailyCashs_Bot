from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
import config
from data_manager import save_users  # ✅ যুক্ত করা হয়েছে

# ✅ স্পিন দেখানোর ফাংশন
async def show_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # 🧩 Task/Ad Simulation
    await query.edit_message_text(
        text="🧩 স্পিন করার আগে একটি টাস্ক কমপ্লিট করুন (যেমন: অ্যাড দেখুন)... ✅"
    )

    # 🎯 স্পিন ইমেজ সহ মেসেজ
    await context.bot.send_photo(
        chat_id=user_id,
        photo="https://i.ibb.co/7PgkQ0d",  # ✅ স্পিন ইমেজ
        caption="🎯 স্পিন করে কয়েন জিতুন!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎡 Spin Now", callback_data="do_spin")]
        ])
    )

# ✅ স্পিন কার্যকর করার ফাংশন
async def do_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # 🎰 র‍্যান্ডম রিওয়ার্ড বাছাই
    reward = random.choice(config.SPIN_REWARDS)
    config.USERS[user_id]["coins"] += reward

    # 🪙 রেফার বোনাস গণনা ও অ্যাড
    for referrer_id, data in config.USERS.items():
        if user_id in data.get("referrals", []):
            bonus = int(reward * config.REFER_PERCENT)
            data["coins"] += bonus
            data["ref_bonus"] = data.get("ref_bonus", 0) + bonus

    # ✅ সেভ করে দাও
    save_users(config.USERS)

    # 🎉 রেজাল্ট মেসেজ
    await query.edit_message_text(
        text=f"🎉 আপনি স্পিন করে {reward} 🪙 কয়েন পেয়েছেন!\n\n💰 Wallet: {config.USERS[user_id]['coins']} 🪙",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 আবার স্পিন করুন", callback_data="spin")],
            [InlineKeyboardButton("🏠 মেইন মেনু", callback_data="open_menu")]
        ])
    )
    
