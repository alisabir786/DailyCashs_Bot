import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data_manager import get_user_data, update_user_data

# সাত দিনের চেকইন রিওয়ার্ড
REWARDS = [4, 8, 16, 32, 72, 90, 120]

def get_day_index(last_checkin: str) -> int:
    today = datetime.date.today()
    if not last_checkin:
        return 0
    last_date = datetime.datetime.strptime(last_checkin, "%Y-%m-%d").date()
    if last_date == today:
        return -1  # Already checked in today
    delta = (today - last_date).days
    return 0 if delta > 1 else 1  # Reset if gap >1

async def daily_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    last_checkin = user_data.get("last_checkin")
    day = user_data.get("checkin_day", 0)

    checkin_index = get_day_index(last_checkin)
    if checkin_index == -1:
        await query.answer("✅ You've already checked in today!", show_alert=True)
        return

    if checkin_index == 0:
        day = 0  # reset day if missed a day

    # Coin Reward দিন
    if day < len(REWARDS):
        reward = REWARDS[day]
        user_data["wallet"] = user_data.get("wallet", 0) + reward
        user_data["last_checkin"] = datetime.date.today().strftime("%Y-%m-%d")
        user_data["checkin_day"] = day + 1
        update_user_data(user_id, user_data)

        # UI Message
        msg = (
            f"🎁 *Daily Check-in*\n\n"
            f"📅 Day {day+1} Check-in Successful!\n"
            f"💰 You've earned: *{reward} coins*\n"
            f"🧮 Total Wallet: *{user_data['wallet']} coins*"
        )
    else:
        msg = "✅ You've completed all 7 days! Check-in streak will reset tomorrow."
        user_data["checkin_day"] = 0
        update_user_data(user_id, user_data)

    keyboard = [[InlineKeyboardButton("🔙 Back to Home", callback_data="home")]]
    await query.edit_message_text(
        text=msg,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
