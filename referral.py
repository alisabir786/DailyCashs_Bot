from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from data_manager import get_user_data, update_user_data
from spin import mark_task_done_for_spin

BONUS_DIRECT = 10
BONUS_PERCENT = 0.10  # 10%

# 🔗 Show refer link
async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    link = f"https://t.me/{context.bot.username}?start={user_id}"

    user_data = get_user_data(user_id)
    team = user_data.get("ref_team", [])

    msg = (
        f"👥 *Refer & Earn!*\n\n"
        f"🔗 Your Link:\n{link}\n\n"
        f"💰 Earn {BONUS_DIRECT} coins + 10% lifetime income\n"
        f"👤 Total Referrals: {len(team)}"
    )

    await update.callback_query.edit_message_text(
        text=msg,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Home", callback_data="home")]
        ])
    )

# 🔄 Handle New Referral
def handle_referral(user_id: int, ref_id: int):
    if user_id == ref_id:
        return

    user_data = get_user_data(user_id)
    if user_data.get("referred_by"):
        return

    ref_data = get_user_data(ref_id)

    # Bonus to new user
    user_data["wallet"] += BONUS_DIRECT
    user_data["referred_by"] = ref_id
    update_user_data(user_id, user_data)

    # Bonus to referrer
    ref_data["wallet"] += BONUS_DIRECT
    ref_data.setdefault("ref_team", []).append(user_id)
    update_user_data(ref_id, ref_data)

    mark_task_done_for_spin(user_id)
    mark_task_done_for_spin(ref_id)
    
