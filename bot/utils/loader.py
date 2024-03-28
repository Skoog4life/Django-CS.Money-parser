from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN_API = os.environ.get("TOKEN_API")

loop = asyncio.get_event_loop()
bot = Bot(TOKEN_API)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
logging.basicConfig(level=logging.INFO)
