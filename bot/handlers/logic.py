import asyncio

from aiogram import types

from bot.utils.loader import bot, dp
from bot.utils.csmoney_parser import parser

from bot.models import TelegramUser, FoundItem
from asgiref.sync import sync_to_async
from bot.keyboards import keyboard

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FiniteStateMachine(StatesGroup):
    check = State()
    profit = State()
    create_user = State()
    update = State()
    start_notifier = State()
    stop_notifier = State()
    staff_add = State()
    staff_remove = State()

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
    if await sync_to_async(user_request.has_superuser_status)():
        await bot.send_message(message.chat.id, "Hello, superuser", reply_markup=keyboard.admin_keyboard)
    elif await sync_to_async(user_request.has_staff_status)():
        await bot.send_message(message.chat.id, "Hello, staff member", reply_markup=keyboard.staff_keyboard)
    else:
        await bot.send_message(message.chat.id, "Hello", reply_markup=keyboard.user_keyboard)

@dp.message_handler(commands=['cancel'], state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.reply('Successfully canceled.')