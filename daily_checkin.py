import datetime
from aiogram import types
from config import dp
from data_manager import (
    get_user,
    update_user,
    has_checked_in_today,
    reward_referrer,
)

# ৭ দিনের রিওয়ার্ড তালিকা
CHECKIN_REWARDS = [4, 8, 16, 32, 72, 90, 120]

@dp.callback_query_handler(lambda c: c.data == "checkin")
async def daily_checkin(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user = get_user(user_id)

    if not user:
        await callback_query.answer("❌ ইউজার পাওয়া যায়নি।")
        return

    if has_checked_in_today(user_id):
        await callback_query.answer("📅 আপনি আজকে চেক-ইন করেছেন।", show_alert=True)
        return

    # দিন নির্ধারণ
    day = user.get("checkin_day", 0)
    if day >= len(CHECKIN_REWARDS):
        day = 0  # Reset on 8th day

    coins = CHECKIN_REWARDS[day]

    # রিওয়ার্ড দিন
    user["wallet"] += coins
    user["checkin_day"] = day + 1
    user["last_checkin"] = datetime.date.today().strftime("%Y-%m-%d")
    update_user(user_id, user)

    # রেফারার ইনকাম ১০%
    ref_by = user.get("ref_by")
    if ref_by:
        bonus = int(coins * 0.10)
        reward_referrer(ref_by, bonus)

    # মেসেজ
    await callback_query.message.edit_text(
        f"✅ *Day {day + 1} Check-in Successful!*\n"
        f"💰 আপনি পেয়েছেন: *{coins} কয়েন*\n"
        f"🧮 মোট ব্যালেন্স: *{user['wallet']} কয়েন*",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🏠 হোমে ফিরে যান", callback_data="home")
        )
    )
    
