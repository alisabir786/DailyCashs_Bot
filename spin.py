# spin.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
import config

async def show_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Task/Ad simulation
    await query.edit_message_text(
        text="🧩 স্পিন করার আগে একটি টাস্ক কমপ্লিট করুন (যেমন: অ্যাড দেখুন)... ✅",
    )

    # Show spin button
    await context.bot.send_message(
        chat_id=user_id,
        text="🎯 স্পিন করুন এবং 0-100 কয়েন জিতুন!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎡 Spin Now", callback_data="do_spin")]
        ])
    )

async def do_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # স্পিন রিওয়ার্ড র‍্যান্ডম বাছাই
    reward = random.choice(config.SPIN_REWARDS)
    config.USERS[user_id]["coins"] += reward

    await query.edit_message_text(
        text=f"🎉 আপনি স্পিন করে {reward} 🪙 কয়েন পেয়েছেন!\n\n💰 Wallet: {config.USERS[user_id]['coins']} 🪙",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 আবার স্পিন করুন", callback_data="spin")],
            [InlineKeyboardButton("🏠 মেইন মেনু", callback_data="open_menu")]
        ])
    )
def add_referral_bonus(user_id, coin_amount):
    for uid, data in config.USERS.items():
        if user_id in data["referrals"]:
            bonus = int(coin_amount * config.REFER_PERCENT)
            data["coins"] += bonus
add_referral_bonus(user_id, coin_amount)
