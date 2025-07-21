``python
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_manager import get_user

@Client.on_message(filters.command("start"))
async def start(_, message):
    user = get_user(message.from_user.id)
    await message.reply_photo(
        photo="https://telegra.ph/file/277f89e97b6eede112c58.png",  # Custom welcome image
        caption=f"""
👋 স্বাগতম {message.from_user.first_name}!
🎮 খেলুন Spin, Task, Check-in করে আয় করুন।
💰 অটো কয়েন Wallet-এ জমা হবে।

👇 শুরু করতে PLAY চাপুন:
        """,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("▶️ PLAY", callback_data="main_menu")]]
        )
    )
```
