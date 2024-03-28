from aiogram import types
from bot.utils.loader import bot, dp

from bot.handlers import logic, admin, user

from bot.models import TelegramUser, ItemPrice
from bot.keyboards import keyboard
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('/'), state="*")
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):

    callback_data = callback_query.data
    print(callback_data)
    
    if callback_data == '/notify_on':
        await bot.send_message(callback_query.from_user.id, 'Notifications enabled')
        await TelegramUser.objects.filter(pk=callback_query.from_user.id).aupdate(notify=True)
    elif callback_data == '/notify_off':
        await bot.send_message(callback_query.from_user.id, 'Notifications disabled')
        await TelegramUser.objects.filter(pk=callback_query.from_user.id).aupdate(notify=False)
    elif callback_data == '/check':
        await bot.send_message(callback_query.from_user.id, 'Please enter the item name:', reply_markup=keyboard.cancel_keyboard)
        await logic.FiniteStateMachine.check.set()
    elif callback_data == '/profit':
        await bot.send_message(callback_query.from_user.id, 'Please enter the desired profit:', reply_markup=keyboard.cancel_keyboard)
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