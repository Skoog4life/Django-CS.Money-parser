from aiogram import types

from django.contrib.auth.models import User

from bot.utils.loader import bot, dp
from bot.models import TelegramUser, Config
from asgiref.sync import sync_to_async
from bot.handlers import logic

from bot.utils.steam_price_checker import check_item_price

from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageTextIsEmpty


@dp.message_handler(commands=["start_notifier"])
async def start_function(message: types.Message = None, chat_id=None):
    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)

    if await sync_to_async(user_request.has_staff_status)():
        if await logic.start_notifier():
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
        if await logic.stop_notifier():
            await bot.send_message(chat_id=chat_id, text="Notifier stopped")
        else:
            await bot.send_message(chat_id=chat_id, text="Notifier is already stopped")
    else:
        await bot.send_message(chat_id=chat_id, text="You do not have enough permissions")


@dp.message_handler(commands=["update"])
@dp.message_handler(state=logic.FiniteStateMachine.update)
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


@dp.message_handler(commands=["time_to_update"])
@dp.message_handler(state=logic.FiniteStateMachine.time_to_update)
async def time_to_update(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    current_state = await state.get_state()
    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        try:
            if current_state is None:
                hours = "".join(message.get_args().split())
            else:
                hours = message.text
                await state.finish()
            try:
                hours = int(hours)
                if hours < 1:
                    raise ValueError
                config = await Config.objects.afirst()
                await sync_to_async(config.set_time_to_update)(hours)
                await message.reply(f"Time to update set to {hours} hours")
            except ValueError:
                await bot.send_message(
                    chat_id=message.from_user.id, text="You need to provide a number greater than 0"
                )
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You need to provide a number greater than 0. Use the command like this: /time_to_update <hours>",
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["page_count"])
@dp.message_handler(state=logic.FiniteStateMachine.page_count)
async def page_count(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    current_state = await state.get_state()
    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        try:
            if current_state is None:
                count = "".join(message.get_args().split())
            else:
                count = message.text
                await state.finish()
            try:
                count = int(count)
                if count < 1:
                    raise ValueError
                config = await Config.objects.afirst()
                await sync_to_async(config.set_page_count)(count)
                await message.reply(f"Page count set to {count}")
            except ValueError:
                await bot.send_message(
                    chat_id=message.from_user.id, text="You need to provide a number greater than 0"
                )
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You need to provide a number greater than 0. Use the command like this: /page_count <count>",
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["csmoney_discount"])
@dp.message_handler(state=logic.FiniteStateMachine.csmoney_discount)
async def csmoney_discount(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    current_state = await state.get_state()
    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        try:
            if current_state is None:
                discount = "".join(message.get_args().split())
            else:
                discount = message.text
                await state.finish()
            try:
                discount = int(discount)
                if discount < 0:
                    raise ValueError
                config = await Config.objects.afirst()
                await sync_to_async(config.set_desired_csmoney_allowed_discount)(discount)
                await message.reply(f"Discount set to {discount}")
            except ValueError:
                await bot.send_message(
                    chat_id=message.from_user.id, text="You need to provide a number greater than or equal to 0"
                )
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You need to provide a number greater than or equal to 0. Use the command like this: /csmoney_discount <discount>",
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["staff_add"])
@dp.message_handler(state=logic.FiniteStateMachine.staff_add)
async def staff_add(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    current_state = await state.get_state()
    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
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
                    await sync_to_async(telegram_user.staff_status)(True)
                    await bot.send_message(chat_id=message.from_user.id, text="User is now staff")
                else:
                    await bot.send_message(chat_id=message.from_user.id, text="User is already staff")
            else:
                await bot.send_message(chat_id=message.from_user.id, text="User not found")
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You need to provide an user id. Use the command like this: /staff <id>",
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


@dp.message_handler(commands=["staff_remove"])
@dp.message_handler(state=logic.FiniteStateMachine.staff_remove)
async def staff_remove(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)

    current_state = await state.get_state()
    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        try:
            if current_state is None:
                id = "".join(message.get_args().split())
            else:
                id = message.text
                await state.finish()
            telegram_user = await TelegramUser.objects.filter(chat_id=id).afirst()
            telegram_user_user = await sync_to_async(lambda: telegram_user.user)()
            if telegram_user and telegram_user_user:
                if await sync_to_async(telegram_user.has_staff_status)():
                    await sync_to_async(telegram_user.staff_status)(False)
                    await bot.send_message(chat_id=message.from_user.id, text="User is no longer staff")
                else:
                    await bot.send_message(chat_id=message.from_user.id, text="User is not staff")
            else:
                await bot.send_message(chat_id=message.from_user.id, text="User not found")
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You need to provide an user id. Use the command like this: /staff <id>",
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text="Try again")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="You do not have enough permissions")


# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('a/'))
# async def process_callback_button(callback_query: types.CallbackQuery):

#     callback_data = callback_query.data[1::]

#     if callback_data == '/update':
#         await bot.send_message(callback_query.from_user.id, "Please enter the item name:")
#         await FiniteStateMachine.update.set()
#     elif callback_data == '/start_notifier':
#         await start_function(chat_id=callback_query.from_user.id)
#     elif callback_data == '/stop_notifier':
#         await stop_function(chat_id=callback_query.from_user.id)
#     elif callback_data == '/staff':
#         await bot.send_message(callback_query.from_user.id, "Please enter the user id:")
#         await FiniteStateMachine.staff.set()

#     await callback_query.answer()
