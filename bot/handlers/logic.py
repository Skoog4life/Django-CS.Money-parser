import asyncio

from aiogram import types

from bot.utils.loader import bot, dp
from bot.utils.csmoney_parser import parser

from bot.models import TelegramUser, FoundItem
from asgiref.sync import sync_to_async
from bot.keyboards import user_keyboard

stop = False

async def notifier():
    while stop == False:     
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
        await asyncio.sleep(5)

async def start_notifier():
    global stop
    if stop == True:
        stop = False
        asyncio.create_task(notifier())
        return True
    return False

async def stop_notifier():
    global stop
    if stop == False:
        stop = True
        return True
    return False

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_request, _ = await TelegramUser.objects.aget_or_create(chat_id=message.from_user.id)
    if await sync_to_async(user_request.has_staff_status)():
        await bot.send_message(message.chat.id, "Hello, staff member", reply_markup=user_keyboard.admin_keyboard)
    else:
        await bot.send_message(message.chat.id, "Hello", reply_markup=user_keyboard.user_keyboard)

