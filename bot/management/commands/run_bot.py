from django.core.management.base import BaseCommand
from bot.utils import csmoney_parser
from bot.utils.loader import bot, dp, loop
from bot.utils.csmoney_parser import parser
from bot.utils.steam_price_checker import check_item_price

from aiogram import executor, types
import asyncio

from bot.handlers import logic


async def on_startup(_):
    print("Bot started")
    asyncio.create_task(logic.notifier())


# async def on_shutdown(_):

#     logic.stop = False
#     dp.stop_polling()
#     await dp.storage.close()
#     await dp.storage.wait_closed()


class Command(BaseCommand):
    help = "Start telegram bot"

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
