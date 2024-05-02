import os
import dotenv
from loader import logger

if not dotenv.find_dotenv():
    logger.critical(".env file does not exists in root directory.")
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    dotenv.load_dotenv()
    logger.info(".env bot token loaded.")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WORKERS_GROUP_ID = int(os.getenv("WORKERS_GROUP_ID"))
TEST_PAYMENT_TOKEN = os.getenv("TEST_PAYMENT_TOKEN")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
