from aiogram import types
from asgiref.sync import sync_to_async
from bot.utils.loader import bot, dp

from bot.handlers import logic, admin, user

from bot.models import TelegramUser, ItemPrice, Config
from bot.keyboards import keyboard
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('/'), state="*")
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):

    callback_data = callback_query.data
    config = await Config.objects.afirst()
    telegram_user = await TelegramUser.objects.filter(pk=callback_query.from_user.id).afirst()
    
    if callback_data == '/notify_on':
        await bot.send_message(callback_query.from_user.id, 'Notifications enabled')
        await sync_to_async(telegram_user.notify_on)()
    elif callback_data == '/notify_off':
        await bot.send_message(callback_query.from_user.id, 'Notifications disabled')        
        await sync_to_async(telegram_user.notify_off)()
    elif callback_data == '/check':
        await bot.send_message(callback_query.from_user.id, 'Please enter the item name:', reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.check.set()
    elif callback_data == '/profit':
        current_profit = await sync_to_async(telegram_user.get_desired_profit)()
        await bot.send_message(callback_query.from_user.id, f"Current profit: {current_profit}%\nPlease enter the desired profit:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.profit.set()
    elif callback_data == '/create_user':
        await bot.send_message(callback_query.from_user.id, 'Please enter the username and the password:', reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.create_user.set()
    elif callback_data == '/update':
        await bot.send_message(callback_query.from_user.id, "Please enter the item name:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.update.set()
    elif callback_data == '/start_notifier':
        await admin.start_function(chat_id=callback_query.from_user.id)
    elif callback_data == '/stop_notifier':
        await admin.stop_function(chat_id=callback_query.from_user.id)
    elif callback_data == '/parse_on_start_on':
        await bot.send_message(callback_query.from_user.id, "Parsing on start enabled")
        await sync_to_async(config.set_parse_on_start)(True)
    elif callback_data == '/parse_on_start_off':
        await bot.send_message(callback_query.from_user.id, "Parsing on start disabled")
        await sync_to_async(config.set_parse_on_start)(False)
    elif callback_data == '/time_to_update':
        current_time = await sync_to_async(config.get_time_to_update)()
        await bot.send_message(callback_query.from_user.id, f"Current time to update: {current_time}\nPlease enter the time in hours:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.time_to_update.set()
    elif callback_data == '/page_count':
        current_page_count = await sync_to_async(config.get_page_count)()
        await bot.send_message(callback_query.from_user.id, f"Current page count: {current_page_count}\nPlease enter the page count:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.page_count.set()
    elif callback_data == '/csmoney_discount':
        current_discount = await sync_to_async(config.get_csmoney_allowed_discount)()
        await bot.send_message(callback_query.from_user.id, f"Current discount: {current_discount}\nPlease enter the desired discount:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.csmoney_discount.set()
    elif callback_data == '/staff_add':
        await bot.send_message(callback_query.from_user.id, "Please enter the user id:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.staff_add.set()
    elif callback_data == '/staff_remove':
        await bot.send_message(callback_query.from_user.id, "Please enter the user id:", reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.staff_remove.set()   
    elif callback_data == '/cancel':
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await bot.send_message(callback_query.from_user.id, 'Successfully canceled')    
         
    await callback_query.answer()