import asyncio
from loguru import logger

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from loader import bot


@logger.catch()
async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    try:
        logger.success("Bot is working")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical("Bot stopped")
    
    