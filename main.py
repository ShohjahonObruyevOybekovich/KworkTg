import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.enums import ParseMode

from db.connect import  engine
from db.model import Base
from dispatcher import TOKEN, dp
from bot.handlers import *

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    Base.metadata.create_all(engine)
    asyncio.run(main())