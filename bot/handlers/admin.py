from turtle import st

from aiogram import types

from django.contrib.auth.models import User

from bot.utils.loader import bot, dp
from bot.models import TelegramUser
from asgiref.sync import sync_to_async
from .logic import notifier, stop_notifier, start_notifier

from bot.utils.steam_price_checker import check_item_price


@dp.message_handler(commands=["start_notifier"])
async def start_function(message: types.Message = None):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    if await sync_to_async(user_request.has_staff_status)():
        if await start_notifier():
            await bot.send_message(chat_id=message.from_user.id, text="Notifier started")
        else:
            await bot.send_message(chat_id=message.from_user.id, text="Notifier is already running")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["stop_notifier"])
async def start_function(message: types.Message = None):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    if await sync_to_async(user_request.has_staff_status)():
        if await stop_notifier():
            await bot.send_message(chat_id=message.from_user.id, text="Notifier stopped")
        else:
            await bot.send_message(chat_id=message.from_user.id, text="Notifier is already stopped")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["update"])
async def update_price(message: types.Message):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    if await sync_to_async(user_request.has_staff_status)():
        try:
            item_name = " ".join(message.get_args().split())
            # await message.reply(f'{item_name}')
            price = await check_item_price(item_name=item_name, update=True)
            await message.reply(f"Price of {item_name} is {price}")
        except:
            await message.reply("Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    if await sync_to_async(user_request.has_staff_status)():
        try:
            id = "".join(message.get_args().split())
            telegram_user = await TelegramUser.objects.filter(chat_id=id).afirst()
            if telegram_user and telegram_user.user:
                if not await sync_to_async(telegram_user.has_staff_status)():
                    await sync_to_async(telegram_user.admin_status)(True)
                    await bot.send_message(chat_id=message.from_user.id, text="User is now admin")
                else:
                    await bot.send_message(chat_id=message.from_user.id, text="User is already admin")
            else:
                await bot.send_message(chat_id=message.from_user.id, text="User not found")
        except :
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")
