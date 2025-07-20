# referral.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config


async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = config.USERS.get(user_id, {})

    referral_link = f"https://t.me/{config.BOT_USERNAME.replace('@','')}?start={user_id}"
    referred_users = user.get("referrals", [])
    bonus = user.get("ref_bonus", 0)

    text = (
        f"👥 <b>Refer & Earn</b>\n\n"
        "🔗 <b>Your Refer Link:</b>\n"
        f"<code>{referral_link}</code>\n\n"
        "🎁 <b>On Refer:</b> +10 Coin\n"
        "💸 <b>Lifetime Bonus:</b> 10% of their earnings\n\n"
        f"👫 <b>Total Referrals:</b> {len(referred_users)}\n"
        f"💰 <b>Bonus Earned:</b> {bonus} Coin"
    )

    await query.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
        ])
    )
