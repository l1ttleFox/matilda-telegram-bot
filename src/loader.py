from aiogram import Bot
import config
import db
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

logger.add("/logs/bot.log",
           format="{time} | {level} | {message}",
           level="DEBUG",
           rotation="10 MB",
           compression="zip"
           )

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
db.Base.metadata.create_all(bind=db.engine)
