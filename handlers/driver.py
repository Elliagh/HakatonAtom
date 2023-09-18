from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, F, Router
from aiogram.types import Message

from kb import change_info_kb, base_kb
from db import ManagerCars
from db import Car
import db

driver_router = Router()


#TODO Выбор машины

@driver_router.message(F.text == "Driver")
async def driver_hello(msg: Message):

    await msg.answer("Пока еще не готово")