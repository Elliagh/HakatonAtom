from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


admin_menu = [
    [KeyboardButton(text="Add new car")],
    [KeyboardButton(text="Change car info")],
    [KeyboardButton(text="Delete car")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)
