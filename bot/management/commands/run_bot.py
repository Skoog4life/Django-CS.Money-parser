from django.core.management.base import BaseCommand
from bot.utils.loader import dp

from aiogram import executor
import asyncio

from bot.models import Config

def initialize_config():
    if not Config.objects.exists():
        Config.objects.create()

initialize_config()

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
