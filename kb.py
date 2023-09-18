from aiogram.types import KeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


admin_menu = [
    [KeyboardButton(text="Add new car")],
    [KeyboardButton(text="Change car info")],
    [KeyboardButton(text="Delete car")]
]

car_change_info = [
    [KeyboardButton(text="model")],
    [KeyboardButton(text="year_of_realease")],
    [KeyboardButton(text="mileage")],
    [KeyboardButton(text="amount_of_fuel")],
    [KeyboardButton(text="type_of_car")],
    [KeyboardButton(text="type_of_fuel")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)
change_info_kb = ReplyKeyboardMarkup(keyboard=car_change_info, resize_keyboard=True)
