from turtle import st

from aiogram import types

from django.contrib.auth.models import User

from bot.utils.loader import bot, dp
from bot.models import TelegramUser
from asgiref.sync import sync_to_async
from .logic import notifier, stop_notifier, start_notifier

from bot.utils.steam_price_checker import check_item_price

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageTextIsEmpty

class FiniteStateMachine(StatesGroup):
    update = State()
    start_notifier = State()
    stop_notifier = State()
    admin = State()

@dp.message_handler(commands=["start_notifier"])
async def start_function(message: types.Message = None, chat_id=None):
    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)

    if await sync_to_async(user_request.has_staff_status)():
        if await start_notifier():
            await bot.send_message(chat_id=chat_id, text="Notifier started")
        else:
            await bot.send_message(chat_id=chat_id, text="Notifier is already running")
    else:
        await bot.send_message(chat_id=chat_id, text="You do not have enough permissions")


@dp.message_handler(commands=["stop_notifier"])
async def stop_function(message: types.Message = None, chat_id=None):
    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)

    if await sync_to_async(user_request.has_staff_status)():
        if await stop_notifier():
            await bot.send_message(chat_id=chat_id, text="Notifier stopped")
        else:
            await bot.send_message(chat_id=chat_id, text="Notifier is already stopped")
    else:
        await bot.send_message(chat_id=chat_id, text="You do not have enough permissions")


@dp.message_handler(commands=["update"])
@dp.message_handler(state=FiniteStateMachine.update)
async def update_price(message: types.Message, state: FSMContext, chat_id=None):

    current_state = await state.get_state()

    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)

    if await sync_to_async(user_request.has_staff_status)():
        try:
            if current_state is None:
                item_name = " ".join(message.get_args().split())
            else:
                item_name = message.text
                await state.finish()            
            price = await check_item_price(item_name=item_name, update=True)
            await message.reply(f"Price of {item_name} is {price}")
        except MessageTextIsEmpty:
            await message.reply("You need to provide an item name. Use the command like this: /update <item_name>")
        except:
            await message.reply("Try again")
    else:
        await bot.send_message(chat_id=chat_id, text="You do not have enough permissions")


@dp.message_handler(commands=["admin"])
@dp.message_handler(state=FiniteStateMachine.admin)
async def admin(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    current_state = await state.get_state()

    if await sync_to_async(user_request.has_staff_status)():
        try:
            if current_state is None:
                id = "".join(message.get_args().split())
            else:
                id = message.text
                await state.finish()
            telegram_user = await TelegramUser.objects.filter(chat_id=id).afirst()
            telegram_user_user = await sync_to_async(lambda: telegram_user.user)()
            if telegram_user and telegram_user_user:
                if not await sync_to_async(telegram_user.has_staff_status)():
                    await sync_to_async(telegram_user.admin_status)(True)
                    await bot.send_message(chat_id=message.from_user.id, text="User is now admin")
                else:
                    await bot.send_message(chat_id=message.from_user.id, text="User is already admin")
            else:
                await bot.send_message(chat_id=message.from_user.id, text="User not found")
        except MessageTextIsEmpty:
            await bot.send_message(chat_id=message.from_user.id, text="You need to provide an user id. Use the command like this: /admin <id>")
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('a/'))
async def process_callback_button(callback_query: types.CallbackQuery):

    callback_data = callback_query.data[1::]

    if callback_data == '/update':
        await bot.send_message(callback_query.from_user.id, "Please enter the item name:")
        await FiniteStateMachine.update.set()
    elif callback_data == '/start_notifier':
        await start_function(chat_id=callback_query.from_user.id)
    elif callback_data == '/stop_notifier':
        await stop_function(chat_id=callback_query.from_user.id)
    elif callback_data == '/admin':
        await bot.send_message(callback_query.from_user.id, "Please enter the user id:")
        await FiniteStateMachine.admin.set()

    await callback_query.answer()