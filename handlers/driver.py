import random
import string

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, F, Router
from aiogram.types import Message
from kb import change_info_kb, base_kb
from simulator import sim_manager, Simulation

import db
from kb import base_kb, user_kb, cancel_car_kb
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

driver_router = Router()


class SelectCar(StatesGroup):
    license_plate = State()


class DiselectCar(StatesGroup):
    license_plate = State()
    password = State()


@driver_router.message(F.text == "Driver")
async def driver_hello(msg: Message):
    await msg.answer("what are you want to do?", reply_markup=user_kb)


@driver_router.message(F.text == "Select car")
async def select_car(msg: Message, state: FSMContext):
    await state.set_state(SelectCar.license_plate)
    await msg.answer("Напиши номерной знак машины")


@driver_router.message(SelectCar.license_plate)
async def process_license_plate(msg: Message, state: FSMContext):
    await state.update_data(license_plate=msg.text)
    data = await state.get_data()
    await state.clear()
    secret = generate_random_string(15)
    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    car = manager_cars.get_info_by_license_plate(data["license_plate"])
    manager_cars.capture_car(data["license_plate"])
    manager_cars.add_secret(data["license_plate"], secret)

    await msg.answer(info_about_car(car) + "\n" + "pass:" + secret, reply_markup=cancel_car_kb)

    simulation = Simulation(1, 100)
    await sim_manager.add_simulation(msg.from_user.id, simulation)


# Diselect
@driver_router.message(F.text == "Diselect")
async def diselect_car(msg: Message, state: FSMContext):
    await state.set_state(DiselectCar.license_plate)
    await msg.answer("write license_plate")


@driver_router.message(DiselectCar.license_plate)
async def diselect_car(msg: Message, state: FSMContext):
    await state.update_data(license_plate=msg.text)
    await state.set_state(DiselectCar.password)
    await msg.answer("write password")


@driver_router.message(DiselectCar.password)
async def diselect_car(msg: Message, state: FSMContext):
    await state.update_data(password=msg.text)
    data = await state.get_data()
    print(data)
    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    result = manager_cars.deselect_car(data["license_plate"], password=data["password"])
    if result == False:
        await  msg.answer("wrong secret", reply_markup=cancel_car_kb)
    else:
        await  msg.answer("it is all", reply_markup=base_kb)

        sim_manager.stop_simulation(msg.from_user.id)


@driver_router.message(F.text == "Show List available cars")
async def show_list_car(msg: Message, state: FSMContext):
    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    cars = manager_cars.get_all_cars()

    for car in cars:
        await msg.answer(info_about_car(car))

    await  msg.answer("it is all", reply_markup=base_kb)


def info_about_car(car):
    return f"""
        license_plate = {car.license_plate}
        model = {car.model}
        year_of_release = {car.year_of_release}
        mileage = {car.mileage}
        amount_of_fuel = {car.amount_of_fuel}
        type_of_fuel = {car.type_of_fuel}
        type_of_car = {car.type_of_car}"""


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string
