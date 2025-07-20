from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
import random
from data_manager import save_users  # ✅ ফাইলের শুরুতে

# ✅ Utility: Ensure user exists
def ensure_user(user_id):
    if user_id not in config.USERS:
        config.USERS[user_id] = {"coins": 0, "referrals": [], "ref_bonus": 0}

# 🎮 Show Task Menu
async def show_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🧮 Game", callback_data="game_task")],
        [InlineKeyboardButton("🎥 Watch Video", callback_data="video_task")],
        [InlineKeyboardButton("👥 Refer & Earn", callback_data="refer_task")],
        [InlineKeyboardButton("🏠 মেইন মেনু", callback_data="open_menu")]
    ]

    await query.edit_message_text(
        text="🧩 টাস্ক নির্বাচন করুন:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🧮 Game Task
questions = [
    {"q": "2 + 3 = ?", "a": "5"},
    {"q": "4 + 6 = ?", "a": "10"},
    {"q": "7 - 4 = ?", "a": "3"},
    {"q": "3 x 2 = ?", "a": "6"},
    {"q": "10 ÷ 2 = ?", "a": "5"},
]

async def game_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    ensure_user(user_id)

    question = random.choice(questions)
    context.user_data["current_question"] = question

    await context.bot.send_message(
        chat_id=user_id,
        text=f"🧠 প্রশ্ন: {question['q']}\nউত্তর দিন নিচে লিখে:"
    )

async def handle_game_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ensure_user(user_id)
    text = update.message.text.strip()

    if "current_question" not in context.user_data:
        return

    correct_answer = context.user_data["current_question"]["a"]

    if text == correct_answer:
        reward = config.GAME_REWARD
        config.USERS[user_id]["coins"] += reward
        add_referral_bonus(user_id, reward)
        save_users(config.USERS)  # ✅ সেভ করা হয়েছে
        await update.message.reply_text(f"✅ সঠিক উত্তর! আপনি {reward} কয়েন পেলেন 🎉")
    else:
        await update.message.reply_text("❌ ভুল উত্তর! আবার চেষ্টা করুন।")

    context.user_data.pop("current_question", None)

# 🎥 Watch Video Task
video_links = [
    "https://youtu.be/dQw4w9WgXcQ",
    "https://youtu.be/9bZkp7q19f0",
    "https://youtu.be/flex-video-1",
    "https://youtu.be/flex-video-2",
    "https://youtu.be/flex-video-3"
]

async def video_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    ensure_user(user_id)

    links = "\n".join([f"🎥 {i+1}. {link}" for i, link in enumerate(video_links)])
    reward = config.VIDEO_REWARD * len(video_links)
    config.USERS[user_id]["coins"] += reward
    add_referral_bonus(user_id, reward)
    save_users(config.USERS)  # ✅ সেভ করা হয়েছে

    await query.edit_message_text(
        text=f"{links}\n\n✅ ভিডিওগুলো দেখে আপনি {reward} কয়েন পেয়েছেন!"
    )

# 👥 Refer & Earn
async def refer_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_id = user.id
    ensure_user(user_id)

    refer_link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"
    total_refers = len(config.USERS[user_id].get("referrals", []))
    total_earn = total_refers * config.REFER_REWARD

    await query.edit_message_text(
        text=(
            "👥 *Refer & Earn*\n\n"
            f"🔗 আপনার লিংক: `{refer_link}`\n"
            f"💰 প্রতি রেফার: {config.REFER_REWARD} কয়েন + লাইফটাইম {int(config.REFER_PERCENT * 100)}%\n"
            f"👫 মোট রেফার: {total_refers} জন\n"
            f"🪙 আর্ন: {total_earn} কয়েন\n"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 লিংক কপি", url=refer_link)],
            [InlineKeyboardButton("🏠 মেইন মেনু", callback_data="open_menu")]
        ])
    )

# 🔁 Referral Bonus System
def add_referral_bonus(user_id, coin_amount):
    for referrer_id, data in config.USERS.items():
        if user_id in data.get("referrals", []):
            bonus = int(coin_amount * config.REFER_PERCENT)
            data["coins"] += bonus
            data["ref_bonus"] = data.get("ref_bonus", 0) + bonus
            
