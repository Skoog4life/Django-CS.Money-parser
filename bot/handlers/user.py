from aiogram import types

from bot.utils.loader import bot, dp, loop
from bot.models import TelegramUser
from asgiref.sync import sync_to_async

from bot.utils.steam_price_checker import check_item_price

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

@dp.message_handler(commands=['check'])
async def check_price(message: types.Message):
    try:
        item_name = " ".join(message.get_args().split())
        await message.reply(f'{item_name}')        
        price = await check_item_price(item_name=item_name)
        await message.reply(f'Price of {item_name} is {price}')
    except:
        await message.reply('Try again')
