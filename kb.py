from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="Вколол инсулин", callback_data="injected_insulin")]
]
check_kb = InlineKeyboardMarkup(inline_keyboard=menu)

admin_menu = [
    [KeyboardButton(text="Add new car")],
    [KeyboardButton(text="Change car info")],
    [KeyboardButton(text="Delete car")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)
