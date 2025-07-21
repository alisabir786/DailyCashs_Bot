from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from data_manager import get_user_data, update_user_data
from spin import mark_task_done_for_spin
import random

MAX_VIDEO_TASKS = 5
MAX_GAME_TASKS = 5
REWARD_PER_TASK = 5

# 📺 ভিডিও Task
async def watch_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    done = user_data.get("video_tasks", 0)
    if done >= MAX_VIDEO_TASKS:
        await query.answer("✅ All video tasks completed today!", show_alert=True)
        return

    user_data["video_tasks"] = done + 1
    user_data["wallet"] += REWARD_PER_TASK
    update_user_data(user_id, user_data)
    mark_task_done_for_spin(user_id)

    await query.edit_message_text(
        f"🎥 You watched a video and earned {REWARD_PER_TASK} coins!\n"
        f"📦 Total wallet: {user_data['wallet']} coins",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 Play Game", callback_data="game_task")],
            [InlineKeyboardButton("🔙 Back", callback_data="home")]
        ])
    )

# 🎮 Game Task (Simple math)
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    done = user_data.get("game_tasks", 0)
    if done >= MAX_GAME_TASKS:
        await query.answer("🎮 Game limit reached today!", show_alert=True)
        return

    # Generate math problem
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    answer = a + b

    context.user_data["game_answer"] = answer
    user_data["game_tasks"] = done + 1
    update_user_data(user_id, user_data)

    await query.edit_message_text(
        f"🧠 Solve this:\n\n`{a} + {b} = ?`\n\n👉 Reply the answer here:",
        parse_mode="Markdown"
    )

# 🎮 Game Answer Handler
async def handle_game_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if "game_answer" not in context.user_data:
        return

    correct = context.user_data["game_answer"]
    if text.isdigit() and int(text) == correct:
        user_data = get_user_data(user_id)
        user_data["wallet"] += REWARD_PER_TASK
        update_user_data(user_id, user_data)
        mark_task_done_for_spin(user_id)

        await update.message.reply_text(
            f"✅ Correct! You earned {REWARD_PER_TASK} coins.\n💰 Wallet: {user_data['wallet']} coins"
        )
    else:
        await update.message.reply_text("❌ Wrong answer. Try again later.")

    context.user_data.pop("game_answer", None)
    
