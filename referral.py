from aiogram import types
from data_manager import add_user, get_user, update_balance
from aiogram.dispatcher import FSMContext
from config import dp

@dp.message_handler(commands=['refer'])
async def referral_info(message: types.Message):
    user_id = message.from_user.id
    refer_link = f"https://t.me/{dp.bot.username}?start={user_id}"
    await message.answer(
        f"🔗 আপনার রেফার লিংক:\n{refer_link}\n\n"
        "🎁 প্রতি সফল রেফারে আপনি পাবেন:\n"
        "➤ 10 কয়েন ইনস্ট্যান্ট\n"
        "➤ 10% লাইফটাইম টিম ইনকাম!"
    )

@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username

    args = message.get_args()
    ref_by = int(args) if args.isdigit() and int(args) != user_id else None

    user = get_user(user_id)
    if not user:
        add_user(user_id, name, username, ref_by=ref_by)
        if ref_by:
            update_balance(ref_by, 10)
            await message.bot.send_message(ref_by, f"🎉 আপনি একজন রেফার করেছেন এবং 10 কয়েন পেয়েছেন!")
        await message.answer("✅ আপনি সফলভাবে যুক্ত হয়েছেন!")
    else:
        await message.answer("👋 আপনি আগেই যুক্ত হয়েছেন।")
