from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Define the user buttons
notify_on_button = InlineKeyboardButton('Enable notifications 🔔', callback_data='u/notify_on')
notify_off_button = InlineKeyboardButton('Disable notifications 🔕', callback_data='u/notify_off')
check_button = InlineKeyboardButton('Check price ✅', callback_data='u/check')
profit_button = InlineKeyboardButton('Change profit 💰', callback_data='u/profit')
create_user_button = InlineKeyboardButton('Create user👤🔑', callback_data='u/create_user')

# Define the admin buttons
update_button = InlineKeyboardButton('Update price 🔄', callback_data='a/update')
start_notifier_button = InlineKeyboardButton('Start notifier 🚀', callback_data='a/start_notifier')
stop_notifier_button = InlineKeyboardButton('Stop notifier 🛑', callback_data='a/stop_notifier')
admin_button = InlineKeyboardButton('Add admin 👤➕', callback_data='a/admin')

separator_button = InlineKeyboardButton('✨ Admin commands ✨', callback_data='separator')

user_keyboard = InlineKeyboardMarkup()
user_keyboard.row(notify_on_button, notify_off_button)
user_keyboard.row(check_button, profit_button)
user_keyboard.row(create_user_button)

admin_keyboard = InlineKeyboardMarkup()

admin_keyboard.row(notify_on_button, notify_off_button)
admin_keyboard.row(check_button, profit_button)
admin_keyboard.row(create_user_button)

admin_keyboard.row(separator_button)

admin_keyboard.row(start_notifier_button, stop_notifier_button)
admin_keyboard.row(update_button, admin_button)
