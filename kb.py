from aiogram import types

list_keyboard = types.InlineKeyboardMarkup()
list_keyboard.add(types.InlineKeyboardButton('Список доступных курсов', callback_data='Список'))

choice_keyboard = types.InlineKeyboardMarkup()
choice_keyboard.add(types.InlineKeyboardButton('Доллар > Гривна', callback_data='USD'))
choice_keyboard.add(types.InlineKeyboardButton('Евро > Гривна', callback_data='EUR'))
choice_keyboard.add(types.InlineKeyboardButton('Фунт стерлингов > Гривна', callback_data='GBP')) 
choice_keyboard.add(types.InlineKeyboardButton('Швейцарский франк > Гривна',callback_data='CHF')) 
choice_keyboard.add(types.InlineKeyboardButton('Японская йена > Гривна', callback_data='JPY')) 
choice_keyboard.add(types.InlineKeyboardButton('Kитайский юань > Гривна', callback_data='CNY')) 
choice_keyboard.add(types.InlineKeyboardButton('EUR > USD', callback_data='EUR>USD'))

backup_keyboard = types.InlineKeyboardMarkup()
backup_keyboard.add(types.InlineKeyboardButton('Сменить курс валют',callback_data='Cпиcoк'))