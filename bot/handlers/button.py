from aiogram import types
from asgiref.sync import sync_to_async
from bot.utils.loader import bot, dp

from bot.handlers import logic, admin, user

from bot.models import TelegramUser, Config
from bot.keyboards import keyboard
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("/"), state="*")
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data
    config = await Config.objects.afirst()
    telegram_user = await TelegramUser.objects.filter(pk=callback_query.from_user.id).afirst()
    language = await sync_to_async(telegram_user.get_language)()

    messages = {
        "ua": {
            "/ua": "Мова змінена на українську",
            "/en": "Мова змінена на англійську",
            "/notify_on": "Сповіщення включено",
            "/notify_off": "Сповіщення виключено",
            "/cancel": "Успішно скасовано",
            "/check": "Будь ласка, введіть назву товару:",
            "/profit": "Поточний прибуток: {current_profit}%\nБудь ласка, введіть бажаний прибуток:",
            "/create_user": "Будь ласка, введіть ім'я користувача та пароль:",
            "/change_language": "Виберіть мову",
            "/update": "Будь ласка, введіть назву товару:",
            "/parse_on_start_on": "Автоматичний парсинг при запуску увімкнено",
            "/parse_on_start_off": "Автоматичний парсинг при запуску вимкнено",
            "/time_to_update": "Поточний час оновлення: {current_time}\nБудь ласка, введіть час у годинах:",
            "/page_count": "Поточна кількість сторінок: {current_page_count}\nБудь ласка, введіть кількість сторінок:",
            "/csmoney_discount": "Поточна знижка: {current_discount}\nБудь ласка, введіть бажану знижку:",
            "/steam_allowed_profit": "Поточний прибуток: {current_profit}\nБудь ласка, введіть бажаний прибуток:",
            "/staff_add": "Будь ласка, введіть ідентифікатор користувача:",
            "/staff_remove": "Будь ласка, введіть ідентифікатор користувача:",
            "language_keyboard": keyboard.ua_language_keyboard,
            "cancel_keyboard": keyboard.ua_cancel_keyboard,
        },
        "en": {
            "/ua": "Language changed to Ukrainian",
            "/en": "Language changed to English",
            "/notify_on": "Notifications enabled",
            "/notify_off": "Notifications disabled",
            "/cancel": "Successfully canceled",
            "/check": "Please enter the item name:",
            "/profit": "Current profit: {current_profit}%\nPlease enter the desired profit:",
            "/create_user": "Please enter the username and the password:",
            "/change_language": "Choose your language",
            "/update": "Please enter the item name:",
            "/parse_on_start_on": "Parsing on start enabled",
            "/parse_on_start_off": "Parsing on start disabled",
            "/time_to_update": "Current time to update: {current_time}\nPlease enter the time in hours:",
            "/page_count": "Current page count: {current_page_count}\nPlease enter the page count:",
            "/csmoney_discount": "Current discount: {current_discount}\nPlease enter the desired discount:",
            "/steam_allowed_profit": "Current profit: {current_profit}\nPlease enter the desired profit:",
            "/staff_add": "Please enter the user id:",
            "/staff_remove": "Please enter the user id:",
            "language_keyboard": keyboard.en_language_keyboard,
            "cancel_keyboard": keyboard.en_cancel_keyboard,
        },
    }

    if callback_data == "/notify_on":
        await bot.send_message(callback_query.from_user.id, messages[language][callback_data])
        await sync_to_async(telegram_user.notify_on)()
    elif callback_data == "/notify_off":
        await bot.send_message(callback_query.from_user.id, messages[language][callback_data])
        await sync_to_async(telegram_user.notify_off)()
    elif callback_data == "/check":
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data],
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.check.set()
    elif callback_data == "/profit":
        current_profit = await sync_to_async(telegram_user.get_desired_profit)()
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data].format(current_profit=current_profit),
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.profit.set()
    elif callback_data == "/create_user":
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data],
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.create_user.set()
    elif callback_data == "/change_language":
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data],
            reply_markup=messages[language]["language_keyboard"],
        )
    elif callback_data == "/ua":
        await bot.send_message(callback_query.from_user.id, "Мова змінена на українську")
        await sync_to_async(telegram_user.set_language)("ua")
    elif callback_data == "/en":
        await bot.send_message(callback_query.from_user.id, "Language changed to English")
        await sync_to_async(telegram_user.set_language)("en")
    elif callback_data == "/help":
        await user.help(chat_id=callback_query.from_user.id)
    elif callback_data == "/update":
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data],
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.update.set()
    elif callback_data == "/start_notifier":
        await admin.start_function(chat_id=callback_query.from_user.id)
    elif callback_data == "/stop_notifier":
        await admin.stop_function(chat_id=callback_query.from_user.id)
    elif callback_data == "/parse_on_start_on":
        await bot.send_message(callback_query.from_user.id, messages[language][callback_data])
        await sync_to_async(config.set_parse_on_start)(True)
    elif callback_data == "/parse_on_start_off":
        await bot.send_message(callback_query.from_user.id, messages[language][callback_data])
        await sync_to_async(config.set_parse_on_start)(False)
    elif callback_data == "/time_to_update":
        current_time = await sync_to_async(config.get_time_to_update)()
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data].format(current_time=current_time),
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.time_to_update.set()
    elif callback_data == "/page_count":
        current_page_count = await sync_to_async(config.get_page_count)()
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data].format(current_page_count=current_page_count),
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.page_count.set()
    elif callback_data == "/csmoney_discount":
        current_discount = await sync_to_async(config.get_csmoney_allowed_discount)()
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data].format(current_discount=current_discount),
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.csmoney_discount.set()
    elif callback_data == "/steam_allowed_profit":
        current_profit = await sync_to_async(config.get_steam_allowed_profit)()
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data].format(current_profit=current_profit),
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.steam_allowed_profit.set()
    elif callback_data == "/staff_add":
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data],
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.staff_add.set()
    elif callback_data == "/staff_remove":
        await bot.send_message(
            callback_query.from_user.id,
            messages[language][callback_data],
            reply_markup=messages[language]["cancel_keyboard"],
        )
        await logic.FiniteStateMachine.staff_remove.set()
    elif callback_data == "/cancel":
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await bot.send_message(callback_query.from_user.id, messages[language][callback_data])

    await callback_query.answer()
