from aiogram.types import KeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

user_menu = [
    [KeyboardButton(text="Select car")],
    [KeyboardButton(text="Show List available cars")]
]

cancel_capture_car = [
    [KeyboardButton(text="Diselect")]
]

auth_menu = [
    [KeyboardButton(text="Register")],
    [KeyboardButton(text="Login")],
    [KeyboardButton(text="LoginAsAdmin")]
]

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
    [KeyboardButton(text="type_of_fuel")],
    [KeyboardButton(text="Отмена")]
]

base_menu = [
    [KeyboardButton(text="Driver")],
    [KeyboardButton(text="Admin")]
]

auth_kb = ReplyKeyboardMarkup(keyboard=auth_menu, resize_keyboard=True)
cancel_car_kb = ReplyKeyboardMarkup(keyboard=cancel_capture_car, resize_keyboard=True)
user_kb = ReplyKeyboardMarkup(keyboard=user_menu, resize_keyboard=True)
admin_kb = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)
change_info_kb = ReplyKeyboardMarkup(keyboard=car_change_info, resize_keyboard=True)
base_kb = ReplyKeyboardMarkup(keyboard=base_menu, resize_keyboard=True)
cancel_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отмена")]], resize_keyboard=True)
