from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_manager import get_balance, update_balance
from config import dp

# ✅ উইথড্রাল স্টেট
class WithdrawState(StatesGroup):
    waiting_for_upi = State()
    waiting_for_amount = State()

# ✅ উইথড্রাল শুরু
@dp.message_handler(commands=['withdraw'])
async def start_withdrawal(message: types.Message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    if balance < 2000:
        await message.answer("❌ উইথড্র করতে হলে অন্তত 2000 কয়েন লাগবে।")
        return

    await message.answer("💳 আপনার UPI ID দিন:")
    await WithdrawState.waiting_for_upi.set()

# ✅ UPI গ্রহণ
@dp.message_handler(state=WithdrawState.waiting_for_upi)
async def receive_upi(message: types.Message, state: FSMContext):
    upi = message.text.strip()
    if "@" not in upi:
        await message.answer("❌ সঠিক UPI ID দিন (উদাহরণ: yourupi@bank):")
        return

    await state.update_data(upi=upi)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("₹100 (2000 কয়েন)", "₹300 (6000 কয়েন)", "₹500 (10000 কয়েন)", "₹1000 (20000 কয়েন)")
    await message.answer("🔢 আপনি কত টাকা তুলতে চান?\n\nমিন 2000 কয়েন = ₹100", reply_markup=markup)
    await WithdrawState.waiting_for_amount.set()

# ✅ Amount গ্রহণ ও প্রক্রিয়া
@dp.message_handler(state=WithdrawState.waiting_for_amount)
async def receive_amount(message: types.Message, state: FSMContext):
    amount_map = {
        "₹100 (2000 কয়েন)": 2000,
        "₹300 (6000 কয়েন)": 6000,
        "₹500 (10000 কয়েন)": 10000,
        "₹1000 (20000 কয়েন)": 20000
    }

    coins_required = amount_map.get(message.text)
    if coins_required is None:
        await message.answer("❌ তালিকাভুক্ত অপশন থেকে বেছে নিন।")
        return

    user_id = message.from_user.id
    balance = get_balance(user_id)
    if balance < coins_required:
        await message.answer("❌ আপনার কাছে যথেষ্ট কয়েন নেই।")
        return

    data = await state.get_data()
    upi_id = data["upi"]

    # কয়েন কেটে ফেলা হচ্ছে
    update_balance(user_id, -coins_required)

    await message.answer(
        f"✅ আপনার উইথড্রাল রিকোয়েস্ট সফলভাবে গ্রহণ করা হয়েছে!\n\n"
        f"💳 UPI: `{upi_id}`\n"
        f"💰 অ্যামাউন্ট: {message.text}\n\n"
        "⏳ 24 ঘণ্টার মধ্যে পেমেন্ট সম্পন্ন হবে।",
        parse_mode="Markdown"
    )

    # অ্যাডমিনকে নোটিফাই (প্রয়োজনে টেলিগ্রাম ইউজার আইডি চেঞ্জ করো)
    await dp.bot.send_message(
        6955653010,  # Admin/User ID
        f"📥 নতুন উইথড্রাল রিকোয়েস্ট:\n\n👤 User: {message.from_user.full_name}\n🆔 ID: {user_id}\n💳 UPI: {upi_id}\n💰 Amount: {message.text}"
    )

    await state.finish()
    
