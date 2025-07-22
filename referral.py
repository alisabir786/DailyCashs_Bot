from aiogram import types
from config import dp
from data_manager import (
    add_user,
    get_user,
    update_balance,
    get_balance,
    users_col,
)

# 🎯 /start কমান্ড – রেফার চেক করে নতুন ইউজার যুক্ত করে
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
            await message.bot.send_message(
                ref_by,
                f"🎉 আপনি একজন রেফার করেছেন এবং 10 কয়েন পেয়েছেন!"
            )
        await message.answer("✅ আপনি সফলভাবে যুক্ত হয়েছেন!")
    else:
        await message.answer("👋 আপনি আগেই যুক্ত হয়েছেন।")


# 🔗 /refer কমান্ড – রেফার লিংক দেখায়
@dp.message_handler(commands=["refer"])
async def referral_info(message: types.Message):
    user_id = message.from_user.id
    bot_username = (await dp.bot.get_me()).username
    refer_link = f"https://t.me/{bot_username}?start={user_id}"
    
    await message.answer(
        f"🔗 আপনার রেফার লিংক:\n{refer_link}\n\n"
        "🎁 প্রতি সফল রেফারে আপনি পাবেন:\n"
        "➤ 10 কয়েন ইনস্ট্যান্ট\n"
        "➤ 10% লাইফটাইম টিম ইনকাম!"
    )


# 👥 /team কমান্ড – রেফার করা ইউজার ও তাদের ইনকাম
@dp.message_handler(commands=['team'])
async def view_team(message: types.Message):
    user_id = message.from_user.id

    # আপনি কাদের রেফার করেছেন?
    referrals = list(users_col.find({"ref_by": user_id}))
    count = len(referrals)
    
    if count == 0:
        await message.answer("🙁 আপনি এখনো কাউকে রেফার করেননি।")
        return

    msg = f"👥 আপনি {count} জনকে রেফার করেছেন:\n\n"
    for user in referrals[:10]:  # প্রথম ১০ জন দেখাবে
        uid = user["user_id"]
        name = user.get("name", "Unknown")
        income = get_balance(uid)
        msg += f"🔸 {name} – 💰 ইনকাম: {income} কয়েন\n"
    
    msg += "\n🤑 রেফার করে 10% টিম ইনকাম পান!"
    await message.answer(msg)
    
