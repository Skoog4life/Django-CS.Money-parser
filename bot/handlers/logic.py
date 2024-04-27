import asyncio

from aiogram import types

from bot.utils.loader import bot, dp
from bot.utils.csmoney_parser import parser

from bot.models import TelegramUser, FoundItem, Config
from asgiref.sync import sync_to_async
from bot.keyboards import keyboard

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import RetryAfter


class FiniteStateMachine(StatesGroup):
    check = State()
    profit = State()
    create_user = State()
    update = State()
    start_notifier = State()
    stop_notifier = State()
    time_to_update = State()
    page_count = State()
    csmoney_discount = State()
    staff_add = State()
    staff_remove = State()


stop = not Config.objects.first().parse_on_start


async def notifier():
    while stop == False:
        await parser()
        foundItems = FoundItem.objects.filter(is_sent=False)
        async for user in TelegramUser.objects.filter(notify=True):
            async for item in foundItems:
                try:
                    if item.profit >= user.desired_profit:
                        await bot.send_message(
                            chat_id=user.chat_id,
                            text=f"Name: {item.name}\nProfit: {item.profit}\nSteam Price: {item.steam_price}\nCSMoney Price: {item.csmoney_price}\nLink: {item.link}",
                        )
                except RetryAfter as e:
                    print(f"RetryAfter: {e}")
                    await asyncio.sleep(15)
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
    user_request, new = await TelegramUser.objects.aget_or_create(chat_id=message.from_user.id)
    if new:
        await bot.send_message(message.chat.id, "Choose your language", reply_markup=keyboard.language_keyboard)
    else:
        language = await sync_to_async(user_request.get_language)()
        status = (
            "superuser"
            if await sync_to_async(user_request.has_superuser_status)()
            else "staff"
            if await sync_to_async(user_request.has_staff_status)()
            else "user"
        )
        messages = {
            "ua": {
                "superuser": "Привіт, суперкористувач. Використовуйте /help, щоб дізнатися про команди",
                "staff": "Привіт, член персоналу. Використовуйте /help, щоб дізнатися про команди",
                "user": "Привіт. Використовуйте /help, щоб дізнатися про команди",
            },
            "en": {
                "superuser": "Hello, superuser. Use /help to see about commands",
                "staff": "Hello, staff member. Use /help to see about commands",
                "user": "Hello. Use /help to see about commands",
            },
        }
        keyboards = {
            "ua": {
                "superuser": keyboard.ua_admin_keyboard,
                "staff": keyboard.ua_staff_keyboard,
                "user": keyboard.ua_user_keyboard,
            },
            "en": {
                "superuser": keyboard.en_admin_keyboard,
                "staff": keyboard.en_staff_keyboard,
                "user": keyboard.en_user_keyboard,
            },
        }
        await bot.send_message(message.chat.id, messages[language][status], reply_markup=keyboards[language][status])


@dp.message_handler(commands=["cancel"], state="*")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()
    cancel_messages = {"ua": "Успішно скасовано", "en": "Successfully canceled"}
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.reply(cancel_messages[language])
