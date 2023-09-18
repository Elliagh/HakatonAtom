from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from kb import base_kb

other_router = Router()


@other_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Hi, it's test Fleet Management System, what do you want ?", reply_markup=base_kb)

