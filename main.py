import logging
from telegram.ext import Updater, Dispatcher
from config import Config
from start_handler import setup_start_handler
from callback_handler import setup_callback_handlers
from message_handler import setup_message_handlers

# লগিং কনফিগারেশন
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    updater = Updater(Config.BOT_TOKEN)
    dp = updater.dispatcher
    
    # হ্যান্ডলার সেটআপ
    setup_start_handler(dp)
    setup_callback_handlers(dp)
    setup_message_handlers(dp)
    
    # বট স্টার্ট করুন
    updater.start_polling()
    logger.info("Bot started successfully!")
    updater.idle()

if __name__ == '__main__':
    main()
