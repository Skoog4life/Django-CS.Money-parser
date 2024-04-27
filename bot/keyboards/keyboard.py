from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Define the user buttons
en_notify_on_button = InlineKeyboardButton('Enable notifications 🔔', callback_data='/notify_on')
en_notify_off_button = InlineKeyboardButton('Disable notifications 🔕', callback_data='/notify_off')
en_check_button = InlineKeyboardButton('Check price ✅', callback_data='/check')
en_profit_button = InlineKeyboardButton('Change profit 💰', callback_data='/profit')
en_create_user_button = InlineKeyboardButton('Create user👤🔑', callback_data='/create_user')
en_change_language_button = InlineKeyboardButton('Change language 🌐', callback_data='/change_language')
en_help_button = InlineKeyboardButton('Help ❓', callback_data='/help')

ua_notify_on_button = InlineKeyboardButton('Увімкнути сповіщення 🔔', callback_data='/notify_on')
ua_notify_off_button = InlineKeyboardButton('Вимкнути сповіщення 🔕', callback_data='/notify_off')
ua_check_button = InlineKeyboardButton('Перевірити ціну ✅', callback_data='/check')
ua_profit_button = InlineKeyboardButton('Змінити прибуток 💰', callback_data='/profit')
ua_create_user_button = InlineKeyboardButton('Створити користувача 👤🔑', callback_data='/create_user')
ua_change_language_button = InlineKeyboardButton('Змінити мову 🌐', callback_data='/change_language')
ua_help_button = InlineKeyboardButton('Допомога ❓', callback_data='/help')

# Define the staff buttons
en_update_button = InlineKeyboardButton('Update price 🔄', callback_data='/update')
en_start_notifier_button = InlineKeyboardButton('Start notifier 🚀', callback_data='/start_notifier')
en_stop_notifier_button = InlineKeyboardButton('Stop notifier 🛑', callback_data='/stop_notifier')

ua_update_button = InlineKeyboardButton('Оновити ціну 🔄', callback_data='/update')
ua_start_notifier_button = InlineKeyboardButton('Запустити сповіщувач 🚀', callback_data='/start_notifier')
ua_stop_notifier_button = InlineKeyboardButton('Зупинити сповіщувач 🛑', callback_data='/stop_notifier')

# Define the admin buttons
en_parse_on_start_on = InlineKeyboardButton('Enable parse on start 🟢', callback_data='/parse_on_start_on')
en_parse_on_start_off = InlineKeyboardButton('Disable parse on start 🔴', callback_data='/parse_on_start_off')
en_time_to_update_button = InlineKeyboardButton('Change update time ⏰', callback_data='/time_to_update')
en_page_count_button = InlineKeyboardButton('Change page count 📄', callback_data='/page_count')
en_csmoney_discount_button = InlineKeyboardButton('Change csmoney discound 💰', callback_data='/csmoney_discount')
en_staff_add_button = InlineKeyboardButton('Add staff 👤➕', callback_data='/staff_add')
en_staff_remove_button = InlineKeyboardButton('Remove staff 👤➖', callback_data='/staff_remove')

ua_parse_on_start_on = InlineKeyboardButton('Увімкнути парсинг при запуску 🟢', callback_data='/parse_on_start_on')
ua_parse_on_start_off = InlineKeyboardButton('Вимкнути парсинг при запуску 🔴', callback_data='/parse_on_start_off')
ua_time_to_update_button = InlineKeyboardButton('Змінити час оновлення ⏰', callback_data='/time_to_update')
ua_page_count_button = InlineKeyboardButton('Змінити кількість сторінок 📄', callback_data='/page_count')
ua_csmoney_discount_button = InlineKeyboardButton('Змінити знижку csmoney 💰', callback_data='/csmoney_discount')
ua_staff_add_button = InlineKeyboardButton('Додати персонал 👤➕', callback_data='/staff_add')
ua_staff_remove_button = InlineKeyboardButton('Видалити персонал 👤➖', callback_data='/staff_remove')


# Define the cancel and separator buttons
en_cancel_button = InlineKeyboardButton('Cancel ❌', callback_data='/cancel')
en_staff_separator_button = InlineKeyboardButton('✨ Staff commands ✨', callback_data='/staff_separator')
en_admin_separator_button = InlineKeyboardButton('🧑‍💻 Admin commands 🧑‍💻', callback_data='/admin_separator')

ua_cancel_button = InlineKeyboardButton('Скасувати ❌', callback_data='/cancel')
ua_staff_separator_button = InlineKeyboardButton('✨ Команди персоналу ✨', callback_data='/staff_separator')
ua_admin_separator_button = InlineKeyboardButton('🧑‍💻 Команди адміністратора 🧑‍💻', callback_data='/admin_separator')

# User

en_user_keyboard = InlineKeyboardMarkup()
en_user_keyboard.row(en_notify_on_button, en_notify_off_button)
en_user_keyboard.row(en_check_button, en_profit_button)
en_user_keyboard.row(en_create_user_button)
en_user_keyboard.row(en_change_language_button)
en_user_keyboard.row(en_help_button)

ua_user_keyboard = InlineKeyboardMarkup()
ua_user_keyboard.row(ua_notify_on_button, ua_notify_off_button)
ua_user_keyboard.row(ua_check_button, ua_profit_button)
ua_user_keyboard.row(ua_create_user_button)
ua_user_keyboard.row(ua_change_language_button)
ua_user_keyboard.row(ua_help_button)

# Staff

en_staff_keyboard = InlineKeyboardMarkup()
en_staff_keyboard.row(en_notify_on_button, en_notify_off_button)
en_staff_keyboard.row(en_check_button, en_profit_button)
en_staff_keyboard.row(en_create_user_button)
en_staff_keyboard.row(en_change_language_button)
en_staff_keyboard.row(en_help_button)

en_staff_keyboard.row(en_staff_separator_button)

en_staff_keyboard.row(en_start_notifier_button, en_stop_notifier_button)
en_staff_keyboard.row(en_update_button)

ua_staff_keyboard = InlineKeyboardMarkup()
ua_staff_keyboard.row(ua_notify_on_button, ua_notify_off_button)
ua_staff_keyboard.row(ua_check_button, ua_profit_button)
ua_staff_keyboard.row(ua_create_user_button)
ua_staff_keyboard.row(ua_change_language_button)
ua_staff_keyboard.row(ua_help_button)

ua_staff_keyboard.row(ua_staff_separator_button)

ua_staff_keyboard.row(ua_start_notifier_button, ua_stop_notifier_button)
ua_staff_keyboard.row(ua_update_button)

# Admin

en_admin_keyboard = InlineKeyboardMarkup()
en_admin_keyboard.row(en_notify_on_button, en_notify_off_button)
en_admin_keyboard.row(en_check_button, en_profit_button)
en_admin_keyboard.row(en_create_user_button)
en_admin_keyboard.row(en_change_language_button)
en_admin_keyboard.row(en_help_button)

en_admin_keyboard.row(en_staff_separator_button)

en_admin_keyboard.row(en_start_notifier_button, en_stop_notifier_button)
en_admin_keyboard.row(en_update_button)

en_admin_keyboard.row(en_admin_separator_button)

en_admin_keyboard.row(en_parse_on_start_on, en_parse_on_start_off)
en_admin_keyboard.row(en_time_to_update_button, en_page_count_button)
en_admin_keyboard.row(en_csmoney_discount_button)
en_admin_keyboard.row(en_staff_add_button, en_staff_remove_button)

ua_admin_keyboard = InlineKeyboardMarkup()
ua_admin_keyboard.row(ua_notify_on_button, ua_notify_off_button)
ua_admin_keyboard.row(ua_check_button, ua_profit_button)
ua_admin_keyboard.row(ua_create_user_button)
ua_admin_keyboard.row(ua_change_language_button)
ua_admin_keyboard.row(ua_help_button)

ua_admin_keyboard.row(ua_staff_separator_button)

ua_admin_keyboard.row(ua_start_notifier_button, ua_stop_notifier_button)
ua_admin_keyboard.row(ua_update_button)

ua_admin_keyboard.row(ua_admin_separator_button)

ua_admin_keyboard.row(ua_parse_on_start_on)
ua_admin_keyboard.row(ua_parse_on_start_off)
ua_admin_keyboard.row(ua_time_to_update_button, ua_page_count_button)
ua_admin_keyboard.row(ua_csmoney_discount_button)
ua_admin_keyboard.row(ua_staff_add_button, ua_staff_remove_button)

# Cancel

en_cancel_keyboard = InlineKeyboardMarkup()
en_cancel_keyboard.row(en_cancel_button)

en_language_keyboard = InlineKeyboardMarkup()
language_button_ua = InlineKeyboardButton('Українська 🇺🇦', callback_data='/ua')
language_button_en = InlineKeyboardButton('English 🇬🇧', callback_data='/en')
en_language_keyboard.row(language_button_ua, language_button_en)
en_language_keyboard.row(en_cancel_button)

ua_cancel_keyboard = InlineKeyboardMarkup()
ua_cancel_keyboard.row(ua_cancel_button)

ua_language_keyboard = InlineKeyboardMarkup()
language_button_ua = InlineKeyboardButton('Українська 🇺🇦', callback_data='/ua')
language_button_en = InlineKeyboardButton('English 🇬🇧', callback_data='/en')
ua_language_keyboard.row(language_button_ua, language_button_en)
ua_language_keyboard.row(ua_cancel_button)