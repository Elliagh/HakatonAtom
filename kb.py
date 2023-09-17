from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


admin_menu = [
    [KeyboardButton(text="Add new car")],
    [KeyboardButton(text="Change car info")],
    [KeyboardButton(text="Delete car")]
]

car_change_info = [
    [InlineKeyboardButton(text="Модель машины")],
    [InlineKeyboardButton(text="Год выпуска")],
    [InlineKeyboardButton(text="Пробег")],
    [InlineKeyboardButton(text="Количество топлива")],
    [InlineKeyboardButton(text="Тип машины")],
    [InlineKeyboardButton(text="Тип топлива")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)
change_info_kb = InlineKeyboardMarkup(inline_keyboard=car_change_info)
