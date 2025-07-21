import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from data_manager import get_user_data, update_user_data

SPIN_COST = 1  # প্রতি স্পিনে কয় Task করতে হবে
MAX_REWARD = 100  # স্পিনে সর্বোচ্চ কয়েন

# স্পিন রেজাল্ট তৈরি
def get_spin_result():
    coins = random.choices(
        [0, 5, 10, 15, 20, 30, 40, 50, 75, 100],
        weights=[15, 15, 15, 10, 10, 8, 6, 5, 3, 2]
    )[0]
    return coins

# স্পিন শুরু
async def start_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    # Task check
    tasks_done = user_data.get("spin_tasks_done", 0)
    if tasks_done < SPIN_COST:
        await query.answer("🧩 Complete a task to spin!", show_alert=True)
        return

    # Spin result
    reward = get_spin_result()
    user_data["wallet"] = user_data.get("wallet", 0) + reward
    user_data["spin_tasks_done"] = 0  # reset after spin
    update_user_data(user_id, user_data)

    msg = (
        f"🎯 *Spin Result:*\n\n"
        f"💥 You earned: *{reward} coins!*\n"
        f"💰 Total Wallet: *{user_data['wallet']} coins*"
    )

    keyboard = [[InlineKeyboardButton("🔄 Spin Again", callback_data="spin_again")],
                [InlineKeyboardButton("🔙 Back to Home", callback_data="home")]]
    await query.edit_message_text(
        text=msg,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# স্পিনের আগে টাস্ক কমপ্লিট করলে এটি কল করো
def mark_task_done_for_spin(user_id: https://youtu.be/79pqNVDbxts?si=nr7MD_uGO2E7glct ):
    user_data = get_user_data(user_id)
    user_data["spin_tasks_done"] = user_data.get("spin_tasks_done", 0) + 1
    update_user_data(user_id, user_data)
    
