from aiogram.types import KeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


admin_menu = [
    [KeyboardButton(text="Add new car")],
    [KeyboardButton(text="Change car info")],
    [KeyboardButton(text="Delete car")]
]

car_change_info = [
    [KeyboardButton(text="Модель машины")],
    [KeyboardButton(text="Год выпуска")],
    [KeyboardButton(text="Пробег")],
    [KeyboardButton(text="Количество топлива")],
    [KeyboardButton(text="Тип машины")],
    [KeyboardButton(text="Тип топлива")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)
change_info_kb = ReplyKeyboardMarkup(keyboard=car_change_info, resize_keyboard=True)
