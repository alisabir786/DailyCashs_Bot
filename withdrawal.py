from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import dp
from data_manager import get_balance, update_balance

# 📌 FSM State
class WithdrawState(StatesGroup):
    waiting_for_upi = State()
    waiting_for_confirm = State()

# 📌 Inline Withdraw UI
@dp.message_handler(commands=["withdraw"])
async def handle_withdraw(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)

    if balance < 2000:
        await message.answer("❌ উইথড্র করতে অন্তত 2000 কয়েন লাগবে (₹100)।")
        return

    # Withdrawal options
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("₹100 = 2000", callback_data="withdraw_100"),
        InlineKeyboardButton("₹300 = 6000", callback_data="withdraw_300"),
        InlineKeyboardButton("₹500 = 10000", callback_data="withdraw_500"),
        InlineKeyboardButton("₹1000 = 20000", callback_data="withdraw_1000"),
    )

    await message.answer("💳 আপনি কত টাকা উইথড্র করতে চান?", reply_markup=kb)

# 📌 Callback Handler (amount select)
@dp.callback_query_handler(lambda c: c.data.startswith("withdraw_"))
async def confirm_withdraw(callback_query: types.CallbackQuery, state: FSMContext):
    amount = int(callback_query.data.split("_")[1])
    coins_required = amount * 20
    user_id = callback_query.from_user.id
    balance = get_balance(user_id)

    if balance < coins_required:
        await callback_query.answer("❌ আপনার কাছে যথেষ্ট কয়েন নেই।", show_alert=True)
        return

    await state.update_data(amount=amount, coins_required=coins_required)

    await callback_query.message.edit_text(
        f"🔐 দয়া করে আপনার UPI ID পাঠান\n\n💸 আপনি ₹{amount} উইথড্র করতে যাচ্ছেন।"
    )
    await WithdrawState.waiting_for_upi.set()

# 📌 Receive UPI & confirm
@dp.message_handler(state=WithdrawState.waiting_for_upi)
async def receive_upi(message: types.Message, state: FSMContext):
    upi = message.text.strip()
    if "@" not in upi:
        await message.answer("❌ সঠিক UPI ID দিন (উদাহরণ: yourupi@bank):")
        return

    await state.update_data(upi=upi)
    data = await state.get_data()

    coins_required = data["coins_required"]
    amount = data["amount"]
    user_id = message.from_user.id
    balance = get_balance(user_id)

    if balance < coins_required:
        await message.answer("❌ আপনার কাছে যথেষ্ট কয়েন নেই।")
        await state.finish()
        return

    # কেটে ফেলা হচ্ছে
    update_balance(user_id, -coins_required)

    await message.answer(
        f"✅ উইথড্রাল রিকোয়েস্ট গ্রহণ করা হয়েছে!\n\n"
        f"💳 UPI: `{upi}`\n"
        f"💰 Amount: ₹{amount} ({coins_required} কয়েন)\n"
        f"⏳ ২৪ ঘণ্টার মধ্যে পেমেন্ট হবে।",
        parse_mode="Markdown"
    )

    # Admin Notification
    await dp.bot.send_message(
        6955653010,
        f"📥 নতুন উইথড্রাল:\n\n👤 {message.from_user.full_name}\n🆔 {user_id}\n💳 UPI: {upi}\n💰 Amount: ₹{amount} ({coins_required} কয়েন)"
    )

    await state.finish()
    
