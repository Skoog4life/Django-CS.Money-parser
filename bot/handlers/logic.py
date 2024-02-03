import asyncio

from aiogram import types

from bot.utils.loader import bot, dp, loop
from bot.utils.csmoney_parser import parser

from bot.models import TelegramUser, FoundItem
from asgiref.sync import sync_to_async
import time

stop_notifier = False


async def notifier():
    while stop_notifier == False:    
        start_time = time.time()    
        await parser()
        foundItems = FoundItem.objects.filter(is_sent=False)
        async for user in TelegramUser.objects.filter(notify=True):
            async for item in foundItems:
                if item.profit >= user.desired_profit:
                    await bot.send_message(
                        chat_id=user.chat_id,
                        text=f"Name: {item.name}\nProfit: {item.profit}\nSteam Price: {item.steam_price}\nCSMoney Price: {item.csmoney_price}\nLink: {item.link}"
                    )
        await foundItems.aupdate(is_sent=True)
        finish_time = time.time()-start_time
        print(finish_time)
        await asyncio.sleep(5)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Hello")
    await TelegramUser.objects.aget_or_create(chat_id=message.from_user.id)


@dp.message_handler(commands=["start_notifier"])
async def start_function(message: types.Message = None):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    if await sync_to_async(user_request.has_staff_status)():
        global stop_notifier
        if stop_notifier == True:
            stop_notifier = False
            asyncio.create_task(notifier())
            await bot.send_message(chat_id=message.from_user.id, text="Notifier started")
        else:
            await bot.send_message(chat_id=message.from_user.id, text="Notifier is already running")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["stop_notifier"])
async def start_function(message: types.Message = None):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    if await sync_to_async(user_request.has_staff_status)():
        global stop_notifier
        stop_notifier = True
        await bot.send_message(chat_id=message.from_user.id, text="Notifier stopped")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")
