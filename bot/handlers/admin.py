from aiogram import types

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
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "start": "Сповіщувач почав роботу",
            "running": "Сповіщувач вже працює",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "start": "Notifier started",
            "running": "Notifier is already running",
            "permission": "You do not have enough permissions",
        },
    }

    if await sync_to_async(user_request.has_staff_status)():
        if await logic.start_notifier():
            await bot.send_message(chat_id=chat_id, text=messages[language]["start"])
        else:
            await bot.send_message(chat_id=chat_id, text=messages[language]["running"])
    else:
        await bot.send_message(chat_id=chat_id, text=messages[language]["permission"])


@dp.message_handler(commands=["stop_notifier"])
async def stop_function(message: types.Message = None, chat_id=None):
    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "stop": "Сповіщувач зупинено",
            "stopped": "Сповіщувач вже зупинено",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "stop": "Notifier stopped",
            "stopped": "Notifier is already stopped",
            "permission": "You do not have enough permissions",
        },
    }

    if await sync_to_async(user_request.has_staff_status)():
        if await logic.stop_notifier():
            await bot.send_message(chat_id=chat_id, text=messages[language]["stop"])
        else:
            await bot.send_message(chat_id=chat_id, text=messages[language]["stopped"])
    else:
        await bot.send_message(chat_id=chat_id, text=messages[language]["permission"])


@dp.message_handler(commands=["parse_on_start_on"])
async def parse_on_start_on(message: types.Message = None, chat_id=None):
    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {"on": "Парсинг включено", "already_on": "Парсинг вже включено", "permission": "У вас недостатньо прав"},
        "en": {
            "on": "Parsing enabled",
            "already_on": "Parsing is already enabled",
            "permission": "You do not have enough permissions",
        },
    }

    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        config = await Config.objects.afirst()
        if config.parse_on_start:
            await bot.send_message(chat_id=chat_id, text=messages[language]["already_on"])
        else:
            await sync_to_async(config.set_parse_on_start)(True)
            await bot.send_message(chat_id=chat_id, text=messages[language]["on"])
    else:
        await bot.send_message(chat_id=chat_id, text=messages[language]["permission"])


@dp.message_handler(commands=["parse_on_start_off"])
async def parse_on_start_off(message: types.Message = None, chat_id=None):
    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "off": "Парсинг виключено",
            "already_off": "Парсинг вже виключено",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "off": "Parsing disabled",
            "already_off": "Parsing is already disabled",
            "permission": "You do not have enough permissions",
        },
    }

    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        config = await Config.objects.afirst()
        if not config.parse_on_start:
            await bot.send_message(chat_id=chat_id, text=messages[language]["already_off"])
        else:
            await sync_to_async(config.set_parse_on_start)(False)
            await bot.send_message(chat_id=chat_id, text=messages[language]["off"])
    else:
        await bot.send_message(chat_id=chat_id, text=messages[language]["permission"])


@dp.message_handler(commands=["update"])
@dp.message_handler(state=logic.FiniteStateMachine.update)
async def update_price(message: types.Message, state: FSMContext, chat_id=None):
    current_state = await state.get_state()

    if not chat_id:
        chat_id = message.from_user.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "price": "Ціна {item_name} є {price}",
            "empty": "Вам потрібно надати назву товару. Використовуйте команду так: /update <item_name>",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "price": "Price of {item_name} is {price}",
            "empty": "You need to provide an item name. Use the command like this: /update <item_name>",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

    if await sync_to_async(user_request.has_staff_status)():
        try:
            if current_state is None:
                item_name = " ".join(message.get_args().split())
            else:
                item_name = message.text
                await state.finish()
            price = await check_item_price(item_name=item_name, update=True)
            await message.reply(messages[language]["price"].format(item_name=item_name, price=price))
        except MessageTextIsEmpty:
            await message.reply(messages[language]["empty"])
        except:
            await message.reply(messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=chat_id, text=messages[language]["permission"])


@dp.message_handler(commands=["time_to_update"])
@dp.message_handler(state=logic.FiniteStateMachine.time_to_update)
async def time_to_update(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "set": "Час оновлення встановлено на {hours} години",
            "greater_than_0": "Вам потрібно вказати число більше 0",
            "command_usage": "Вам потрібно вказати число більше 0. Використовуйте команду так: /time_to_update <hours>",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "set": "Time to update set to {hours} hours",
            "greater_than_0": "You need to provide a number greater than 0",
            "command_usage": "You need to provide a number greater than 0. Use the command like this: /time_to_update <hours>",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

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
                await message.reply(messages[language]["set"].format(hours=hours))
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id, text=messages[language]["greater_than_0"])
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=messages[language]["command_usage"],
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=messages[language]["permission"])


@dp.message_handler(commands=["page_count"])
@dp.message_handler(state=logic.FiniteStateMachine.page_count)
async def page_count(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "set": "Кількість сторінок встановлено на {count}",
            "greater_than_0": "Вам потрібно вказати число більше 0",
            "command_usage": "Вам потрібно вказати число більше 0. Використовуйте команду так: /page_count",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "set": "Page count set to {count}",
            "greater_than_0": "You need to provide a number greater than 0",
            "command_usage": "You need to provide a number greater than 0. Use the command like this: /page_count",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

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
                await message.reply(messages[language]["set"].format(count=count))
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id, text=messages[language]["greater_than_0"])
        except MessageTextIsEmpty:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["command_usage"])
        except:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=messages[language]["permission"])


@dp.message_handler(commands=["csmoney_discount"])
@dp.message_handler(state=logic.FiniteStateMachine.csmoney_discount)
async def csmoney_discount(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "set": "Знижка встановлена на {discount}",
            "greater_than_0": "Вам потрібно вказати число більше або рівне 0",
            "command_usage": "Вам потрібно вказати число більше або рівне 0. Використовуйте команду так: /csmoney_discount <discount>",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "set": "Discount set to {discount}",
            "greater_than_0": "You need to provide a number greater than or equal to 0",
            "command_usage": "You need to provide a number greater than or equal to 0. Use the command like this: /csmoney_discount <discount>",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

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
                await message.reply(messages[language]["set"].format(discount=discount))
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id, text=messages[language]["greater_than_0"])
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=messages[language]["command_usage"],
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=messages[language]["permission"])

@dp.message_handler(commands=["steam_allowed_profit"])
@dp.message_handler(state=logic.FiniteStateMachine.steam_allowed_profit)
async def steam_allowed_profit(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "set": "Дозволений прибуток встановлено на {profit}%",
            "command_usage": "Вам потрібно вказати число більше або рівне 0. Використовуйте команду так: /steam_allowed_profit <profit>",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "set": "Allowed profit set to {profit}%",
            "command_usage": "You need to provide a number greater than or equal to 0. Use the command like this: /steam_allowed_profit <profit>",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

    current_state = await state.get_state()
    if (
        await sync_to_async(user_request.has_superuser_status)()
        and await sync_to_async(user_request.has_staff_status)()
    ):
        try:
            if current_state is None:
                profit = "".join(message.get_args().split())
            else:
                profit = message.text
                await state.finish()
            try:
                profit = int(profit)
                if profit < 0:
                    raise ValueError
                config = await Config.objects.afirst()
                await sync_to_async(config.set_steam_allowed_profit)(profit)
                await message.reply(messages[language]["set"].format(profit=profit))
            except ValueError:
                await bot.send_message(chat_id=message.from_user.id, text=messages[language]["greater_than_0"])
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=messages[language]["command_usage"],
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=messages[language]["permission"])

@dp.message_handler(commands=["staff_add"])
@dp.message_handler(state=logic.FiniteStateMachine.staff_add)
async def staff_add(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "now_staff": "Користувач тепер є персоналом",
            "already_staff": "Користувач вже є персоналом",
            "not_found": "Користувача не знайдено",
            "command_usage": "Вам потрібно вказати id користувача. Використовуйте команду так: /staff <id>",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "now_staff": "User is now staff",
            "already_staff": "User is already staff",
            "not_found": "User not found",
            "command_usage": "You need to provide an user id. Use the command like this: /staff <id>",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

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
                    await bot.send_message(chat_id=message.from_user.id, text=messages[language]["now_staff"])
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=messages[language]["already_staff"])
            else:
                await bot.send_message(chat_id=message.from_user.id, text=messages[language]["not_found"])
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You need to provide an user id. Use the command like this: /staff <id>",
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=messages[language]["permission"])


@dp.message_handler(commands=["staff_remove"])
@dp.message_handler(state=logic.FiniteStateMachine.staff_remove)
async def staff_remove(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "you": "Ви не можете видалити себе з персоналу",
            "now_staff": "Користувач більше не є персоналом",
            "not_staff": "Користувач не є персоналом",
            "not_found": "Користувача не знайдено",
            "command_usage": "Вам потрібно вказати id користувача. Використовуйте команду так: /staff <id>",
            "try_again": "Спробуйте ще раз",
            "permission": "У вас недостатньо прав",
        },
        "en": {
            "you": "You can't remove yourself from staff",
            "now_staff": "User is no longer staff",
            "not_staff": "User is not staff",
            "not_found": "User not found",
            "command_usage": "You need to provide an user id. Use the command like this: /staff <id>",
            "try_again": "Try again",
            "permission": "You do not have enough permissions",
        },
    }

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
                if id == user_request.chat_id:
                    await bot.send_message(chat_id=message.from_user.id, text=messages[language]["you"])
                elif await sync_to_async(telegram_user.has_staff_status)():
                    await sync_to_async(telegram_user.staff_status)(False)
                    await bot.send_message(chat_id=message.from_user.id, text=messages[language]["now_staff"])
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=messages[language]["not_staff"])
            else:
                await bot.send_message(chat_id=message.from_user.id, text=messages[language]["not_found"])
        except MessageTextIsEmpty:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=message[language]["command_usage"],
            )
        except:
            await bot.send_message(chat_id=message.from_user.id, text=messages[language]["try_again"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=messages[language]["permission"])
