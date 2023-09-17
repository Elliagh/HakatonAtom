from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from kb import admin_kb

admin_router = Router()


class AddCar(StatesGroup):
    license_plate = State()
    car_model = State()
    year_of_release = State()
    mileage = State()
    amount_of_fuel = State()
    type_of_car = State()
    type_of_fuel = State()

class ChangeCar(StatesGroup):
    pass

class DeleteCar(StatesGroup):
    pass


@admin_router.message(F.text == "Add new car")
async def start_add_car(msg: Message, state: FSMContext):
    await state.set_state(AddCar.license_plate)
    await msg.answer("Напиши номерной знак машины", reply_markup=ReplyKeyboardRemove())

@admin_router.message(AddCar.license_plate)
async def process_license_plate(msg: Message, state: FSMContext):
    await state.update_data(license_plate=msg.text)
    await state.set_state(AddCar.car_model)

    await msg.answer("Напиши модель машины")
    
@admin_router.message(AddCar.car_model)
async def process_car_model(msg: Message, state: FSMContext):
    await state.update_data(car_model=msg.text)
    await state.set_state(AddCar.year_of_release)

    await msg.answer("Напиши год выпуска машины")

@admin_router.message(AddCar.year_of_release)
async def process_year_of_release(msg: Message, state: FSMContext):
    await state.update_data(year_of_release=msg.text)
    await state.set_state(AddCar.mileage)

    await msg.answer("Напиши пробег машины")

@admin_router.message(AddCar.mileage)
async def process_mileage(msg: Message, state: FSMContext):
    await state.update_data(mileage=msg.text)
    await state.set_state(AddCar.amount_of_fuel)

    await msg.answer("Напиши количество топлива в данный момент")

@admin_router.message(AddCar.amount_of_fuel)
async def process_amount_of_fuel(msg: Message, state: FSMContext):
    await state.update_data(amount_of_fuel=msg.text)
    await state.set_state(AddCar.type_of_car)

    kb = [
        [KeyboardButton(text="Каршеринг")],
        [KeyboardButton(text="Такси")],
        [KeyboardButton(text="Доставка")]
    ]

    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await msg.answer("Выбери тип машины", reply_markup=kb)

@admin_router.message(AddCar.type_of_car)
async def process_type_of_car(msg: Message, state: FSMContext):
    await state.update_data(type_of_car=msg.text)
    await state.set_state(AddCar.type_of_fuel)

    kb = [
        [KeyboardButton(text="АИ-92")],
        [KeyboardButton(text="АИ-95")],
        [KeyboardButton(text="АИ-100")]
    ]

    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await msg.answer("Выбери тип топлива", reply_markup=kb)

@admin_router.message(AddCar.type_of_fuel)
async def process_type_of_fuel(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    

    await msg.answer("Машина добавлена в базу данных", reply_markup=admin_kb)    

