from aiogram import types

from bot.utils.loader import bot, dp
from bot.models import TelegramUser, ItemPrice
from asgiref.sync import sync_to_async
from bot.handlers import logic

from django.contrib.auth.models import User
from django.db import IntegrityError

from bot.utils.steam_price_checker import check_item_price

from aiogram.utils.exceptions import MessageTextIsEmpty

from aiogram.dispatcher import FSMContext

from bot.keyboards import keyboard


@dp.message_handler(commands=["notify_on"])
async def notify_on(message: types.Message):
    await TelegramUser.objects.filter(pk=message.from_user.id).aupdate(notify=True)


@dp.message_handler(commands=["notify_off"])
async def notify_off(message: types.Message):
    await TelegramUser.objects.filter(pk=message.from_user.id).aupdate(notify=False)


@dp.message_handler(commands=["profit"])
@dp.message_handler(state=logic.FiniteStateMachine.profit)
async def change_profit(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "set": "Прибуток встановлено на {profit}%",
            "command_usage": "Вам потрібно вказати бажаний прибуток. Використовуйте команду так: /profit <profit>",
            "try_again": "Спробуйте ще раз. Вам потрібно вказати тільки числа.",
        },
        "en": {
            "set": "Profit set to {profit}%",
            "command_usage": "You need to provide the desired profit. Use the command like this: /profit <profit>",
            "try_again": "Try again. You need to provide numbers only.",
        },
    }

    current_state = await state.get_state()
    if current_state is None:
        profit = message.get_args()
    else:
        profit = message.text
        await state.finish()
    try:
        await sync_to_async(user_request.set_desired_profit)(int(profit))
        await message.reply(messages[language]["set"].format(profit=profit))
    except MessageTextIsEmpty:
        await message.reply(messages[language]["command_usage"])
    except:
        await message.reply(messages[language]["try_again"])


@dp.message_handler(commands=["check"])
@dp.message_handler(state=logic.FiniteStateMachine.check)
async def check_price(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "price": "Ціна {item_name} є {price}",
            "not_found": "Товар не знайдено",
            "command_usage": "Вам потрібно вказати назву товару. Використовуйте команду так: /check <item_name>",
            "try_again": "Спробуйте ще раз",
        },
        "en": {
            "price": "Price of {item_name} is {price}",
            "not_found": "Item not found",
            "command_usage": "You need to provide an item name. Use the command like this: /check <item_name>",
            "try_again": "Try again",
        },
    }

    current_state = await state.get_state()
    try:
        if current_state is None:
            item_name = " ".join(message.get_args().split())
        else:
            item_name = message.text
            await state.finish()
        if await ItemPrice.objects.filter(name=item_name).aexists():
            price = await check_item_price(item_name=item_name)
            await message.reply(messages[language]["price"].format(item_name=item_name, price=price))
        else:
            await message.reply(messages[language]["not_found"])
    except MessageTextIsEmpty:
        await message.reply(messages[language]["command_usage"])
    except:
        await message.reply(messages[language]["try_again"])


@dp.message_handler(commands=["create_user"])
@dp.message_handler(state=logic.FiniteStateMachine.create_user)
async def create_user(message: types.Message, state: FSMContext):
    user_request = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    language = await sync_to_async(user_request.get_language)()

    messages = {
        "ua": {
            "created": "Користувач створений",
            "username_exists": "Користувач з цим іменем вже існує",
            "already_exists": "Користувач вже існує",
            "provide_username_password": "Вам потрібно вказати ім'я користувача та пароль.",
        },
        "en": {
            "created": "User created",
            "username_exists": "User with this username already exists",
            "already_exists": "User already exists",
            "provide_username_password": "You need to provide a username and a password.",
        },
    }

    current_state = await state.get_state()
    try:
        if current_state is None:
            username, password = message.get_args().split()
        else:
            username, password = message.text.split()
            await state.finish()
    except ValueError:
        await message.reply(messages[language]["provide_username_password"])
        return
    user_request_user = await sync_to_async(lambda: user_request.user)()
    if not user_request_user:
        try:
            user = await sync_to_async(User.objects.create_user)(username=username, password=password)
            await sync_to_async(user.save)()
            await sync_to_async(user_request.set_user)(user)
            await message.reply(messages[language]["created"])
        except IntegrityError:
            await message.reply(messages[language]["username_exists"])
    else:
        await message.reply(messages[language]["already_exists"])


@dp.message_handler(commands=["help"])
async def help(message: types.Message = None, chat_id=None):
    if chat_id is None:
        chat_id = message.chat.id
    user_request = await TelegramUser.objects.aget(chat_id=chat_id)
    language = await sync_to_async(user_request.get_language)()

    commands = {
        "user": {"ua": "✅ Команди користувача ✅", "en": "✅ User commands ✅"},
        "help": {"ua": "/help - вивести список команд", "en": "/help - show the list of commands"},
        "notify_on": {"ua": "/notify_on - увімкнути сповіщення", "en": "/notify_on - enable notifications"},
        "notify_off": {"ua": "/notify_off - вимкнути сповіщення", "en": "/notify_off - disable notifications"},
        "check": {
            "ua": "/check <назва предмету> - перевірити ціну товару",
            "en": "/check <item name> - check the price of the item",
        },
        "profit": {
            "ua": "/profit <прибуток> - встановити бажаний прибуток в процентах",
            "en": "/profit <profit> - set the desired profit in percentage",
        },
        "create_user": {
            "ua": "/create_user <ім'я> <пароль> - створити користувача",
            "en": "/create_user <username> <password> - create a user",
        },
        "staff": {"ua": "✨ Команди персоналу ✨", "en": "✨ Staff commands ✨"},
        "start_notifier": {
            "ua": "/start_notifier - почати парсинг csmoney та надсилання сповіщень",
            "en": "/start_notifier - start csmoney parse and sending notifications",
        },
        "stop_notifier": {
            "ua": "/stop_notifier - припинити парсинг csmoney та надсилання сповіщень",
            "en": "/stop_notifier - stop csmoney parse and sending notifications",
        },
        "update": {
            "ua": "/update <назва товару> - оновити ціну товару в базі даних",
            "en": "/update <item_name> - update the price of the item in the database",
        },
        "admin": {"ua": "🧑‍💻 Команди адміністратора 🧑‍💻", "en": "🧑‍💻 Admin commands 🧑‍💻"},
        "parse_on_start_on": {
            "ua": "/parse_on_start_on - ввімкнути парсинг при запуску бота",
            "en": "/parse_on_start_on - enable parsing on bot start",
        },
        "parse_on_start_off": {
            "ua": "/parse_on_start_off - вимкнути парсинг при запуску бота",
            "en": "/parse_on_start_off - disable parsing on bot start",
        },
        "time_to_update": {
            "ua": "/time_to_update <години> - встановити час оновлення цін",
            "en": "/time_to_update <hours> - set the time to update prices",
        },
        "page_count": {
            "ua": "/page_count <кількість> - встановити кількість сторінок для парсингу",
            "en": "/page_count <count> - set the number of pages to parse",
        },
        "csmoney_discount": {
            "ua": "/csmoney_discount <знижка> - встановити задовільну знижку на сайті csmoney",
            "en": "/csmoney_discount <discount> - set the desired discount on csmoney site",
        },
        "steam_allowed_profit": {
            "ua": "/steam_allowed_profit <прибуток> - встановити бажаний прибуток на сайті steam",
            "en": "/steam_allowed_profit <profit> - set the desired profit on steam site",
        },
        "staff_add": {
            "ua": "/staff_add <id> - додати користувача до персоналу",
            "en": "/staff_add <id> - add a user to the staff",
        },
        "staff_remove": {
            "ua": "/staff_remove <id> - видалити користувача з персоналу",
            "en": "/staff_remove <id> - remove a user from the staff",
        },
    }

    messages = {
        "ua": {"help": "Доступні команди:\n" + "\n".join(command["ua"] for command in commands.values())},
        "en": {"help": "Available commands:\n" + "\n".join(command["en"] for command in commands.values())},
    }

    if message:
        await message.reply(messages[language]["help"])
    else:
        await bot.send_message(chat_id, messages[language]["help"])
