from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from data_manager import save_users  # ডেটা সেভ করার জন্য দরকার হবে

async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = config.USERS.get(user_id)

    # নতুন ইউজার হলে রেজিস্টার করে ফেলি
    if user is None:
        config.USERS[user_id] = {
            "coins": 0,
            "referrals": [],
            "ref_bonus": 0,
            "first_name": query.from_user.first_name
        }
        user = config.USERS[user_id]
        save_users(config.USERS)  # ইউজার রেজিস্ট্রেশনের পর সেভ করা উচিত

    referral_link = f"https://t.me/{config.BOT_USERNAME.replace('@','')}?start={user_id}"
    referred_users = user.get("referrals", [])
    bonus = user.get("ref_bonus", 0)

    text = (
        f"👥 <b>Refer & Earn</b>\n\n"
        "🔗 <b>Your Referral Link:</b>\n"
        f"<code>{referral_link}</code>\n\n"
        "🎁 <b>On Refer:</b> +10 Coin (for you)\n"
        "💸 <b>Lifetime Bonus:</b> 10% of their earnings\n\n"
        f"👫 <b>Total Referrals:</b> {len(referred_users)}\n"
        f"💰 <b>Bonus Earned:</b> {bonus} 🪙"
    )

    await query.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="open_menu")]
        ])
    )
    
