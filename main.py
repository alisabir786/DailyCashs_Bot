from aiogram import executor
from config import dp

# All Handlers Import
from start_handler import *
from wallet import *
from profile import *
from daily_checkin import *
from spin import *
from task import *
from referral import *
from withdrawal import *

if __name__ == "__main__":
    print("🚀 Bot is running...")
    executor.start_polling(dp, skip_updates=True)
