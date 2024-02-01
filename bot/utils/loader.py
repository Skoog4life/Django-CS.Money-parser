from aiogram import Bot, Dispatcher
import logging
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN_API = os.environ.get('TOKEN_API')

loop = asyncio.get_event_loop()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)        
logging.basicConfig(level=logging.INFO)
