from aiogram import types

from bot.utils.loader import bot, dp, loop
from bot.models import TelegramUser
from asgiref.sync import sync_to_async

@dp.message_handler(commands=['notify_on'])
async def notify_on(message: types.Message):
    await TelegramUser.objects.filter(pk=message.from_user.id).aupdate(notify=True)

@dp.message_handler(commands=['notify_off'])
async def notify_off(message: types.Message):
    await TelegramUser.objects.filter(pk=message.from_user.id).aupdate(notify=False)

@dp.message_handler(commands=['profit'])
async def change_profit(message: types.Message):    
    try:
        user = await TelegramUser.objects.aget(pk=message.from_user.id)
        await sync_to_async(user.set_desired_profit)(int(message.get_args()))
    except:
        await message.reply('Try again')
    