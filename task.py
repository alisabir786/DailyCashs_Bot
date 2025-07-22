from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_manager import log_task, get_today_task_count, update_balance, get_user
from config import dp

# 🎮 গেম টাস্ক (2+3 টাইপ গেম)
@dp.message_handler(commands=["game_task"])
async def game_task(message: types.Message):
    user_id = message.from_user.id
    count = get_today_task_count(user_id, "game")
    if count >= 5:
        await message.answer("❌ আপনি আজকের জন্য ৫টি গেম টাস্ক কমপ্লিট করে ফেলেছেন।")
        return

    await message.answer("🔢 গেম প্রশ্ন: 2 + 3 = ?\nউত্তর দিন।")

# ইউজার রিপ্লাই করে উত্তর দিবে
@dp.message_handler(lambda message: message.text.strip().isdigit() and message.text.strip() in ["5", "৫"])
async def check_game_answer(message: types.Message):
    user_id = message.from_user.id
    count = get_today_task_count(user_id, "game")
    if count >= 5:
        await message.answer("❌ আপনি আজকের জন্য ৫টি গেম টাস্ক কমপ্লিট করে ফেলেছেন।")
        return

    log_task(user_id, "game", 5)
    await message.answer("✅ সঠিক উত্তর! আপনি পেয়েছেন 5 কয়েন 🎉")

# 🎥 ভিডিও টাস্ক (Watch video and reward)
@dp.message_handler(commands=["video_task"])
async def video_task(message: types.Message):
    user_id = message.from_user.id
    count = get_today_task_count(user_id, "video")
    if count >= 5:
        await message.answer("❌ আপনি আজকের জন্য ৫টি ভিডিও টাস্ক করে ফেলেছেন।")
        return

    # ভিডিও বা লিঙ্ক পাঠানো যেতে পারে
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🎬 ভিডিও দেখেছি ✅", callback_data="video_done")
    )
    await message.answer("▶️ নিচের ভিডিওটি দেখুন:\n\nhttps://youtu.be/dQw4w9WgXcQ", reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data == "video_done")
async def video_done_handler(call: types.CallbackQuery):
    user_id = call.from_user.id
    count = get_today_task_count(user_id, "video")
    if count >= 5:
        await call.message.edit_text("❌ আপনি আজকের জন্য ৫টি ভিডিও টাস্ক কমপ্লিট করে ফেলেছেন।")
        return

    log_task(user_id, "video", 5)
    await call.message.edit_text("🎉 ধন্যবাদ! আপনি ভিডিও দেখার জন্য 5 কয়েন পেয়েছেন।")

# 👥 রেফার টাস্ক (Refer friend)
@dp.message_handler(commands=["refer"])
async def refer_task(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    username = message.from_user.username or "your_telegram_id"
    invite_link = f"https://t.me/DailyCashs_Bot?start={user_id}"

    await message.answer(
        f"👥 *রেফার ও আর্ন করুন!*\n\n"
        f"➕ প্রতি রেফারে পাবেন: 10 কয়েন\n"
        f"🎁 রেফার করা ইউজার ইনকাম করলে পাবেন 10% লাইফটাইম বোনাস\n\n"
        f"🔗 আপনার লিঙ্ক:\n`{invite_link}`\n\n"
        f"📢 শেয়ার করুন বন্ধুদের মাঝে!",
        parse_mode="Markdown"
    )
    
