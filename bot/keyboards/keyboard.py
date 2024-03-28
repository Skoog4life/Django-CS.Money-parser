from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Define the user buttons
notify_on_button = InlineKeyboardButton('Enable notifications 🔔', callback_data='/notify_on')
notify_off_button = InlineKeyboardButton('Disable notifications 🔕', callback_data='/notify_off')
check_button = InlineKeyboardButton('Check price ✅', callback_data='/check')
profit_button = InlineKeyboardButton('Change profit 💰', callback_data='/profit')
create_user_button = InlineKeyboardButton('Create user👤🔑', callback_data='/create_user')

# Define the staff buttons
update_button = InlineKeyboardButton('Update price 🔄', callback_data='/update')
start_notifier_button = InlineKeyboardButton('Start notifier 🚀', callback_data='/start_notifier')
stop_notifier_button = InlineKeyboardButton('Stop notifier 🛑', callback_data='/stop_notifier')

# Define the admin buttons
staff_add_button = InlineKeyboardButton('Add staff 👤➕', callback_data='/staff_add')
staff_remove_button = InlineKeyboardButton('Remove staff 👤➖', callback_data='/staff_remove')

cancel_button = InlineKeyboardButton('Cancel ❌', callback_data='/cancel')
separator_button = InlineKeyboardButton('✨ Admin commands ✨', callback_data='/separator')

user_keyboard = InlineKeyboardMarkup()
user_keyboard.row(notify_on_button, notify_off_button)
user_keyboard.row(check_button, profit_button)
user_keyboard.row(create_user_button)

staff_keyboard = InlineKeyboardMarkup()
staff_keyboard.row(notify_on_button, notify_off_button)
staff_keyboard.row(check_button, profit_button)
staff_keyboard.row(create_user_button)

staff_keyboard.row(separator_button)

staff_keyboard.row(start_notifier_button, stop_notifier_button)
staff_keyboard.row(update_button)

admin_keyboard = InlineKeyboardMarkup()
admin_keyboard.row(notify_on_button, notify_off_button)
admin_keyboard.row(check_button, profit_button)
admin_keyboard.row(create_user_button)

admin_keyboard.row(separator_button)

admin_keyboard.row(start_notifier_button, stop_notifier_button)
admin_keyboard.row(staff_add_button, staff_remove_button)
admin_keyboard.row(update_button)

cancel_keyboard = InlineKeyboardMarkup()
cancel_keyboard.row(cancel_button)