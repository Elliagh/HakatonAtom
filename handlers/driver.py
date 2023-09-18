import random
import string
from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, F, Router
from aiogram.types import Message
from kb import change_info_kb, base_kb
from db import ManagerCars
from db import Car
import db
from kb import base_kb, user_kb, cancel_car_kb,auth_kb
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

driver_router = Router()
current_driver = db.User(-1, "test", "qwerty")

class RegisterUser(StatesGroup):
    name = State()
    surname = State()
    password = State()


class LoginUser(StatesGroup):
    name = State()
    password = State()

class SelectCar(StatesGroup):
    license_plate = State()
    driver_id = State()


class DiselectCar(StatesGroup):
    license_plate = State()
    password = State()


# TODO Выбор машины

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
    id = msg.from_user.id
    await state.clear()
    secret = generate_random_string(15)
    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    manager_cars.add_start_time(
        sign_number=data["license_plate"],
        id_user=id,
        time=convert_to_postgresql_datetime(datetime.datetime.now())
    )
    car = manager_cars.get_info_by_license_plate(data["license_plate"])
    manager_cars.capture_car(data["license_plate"])
    manager_cars.add_secret(data["license_plate"], secret)
    await msg.answer(info_about_car(car) + "\n" + "pass:" + secret, reply_markup=cancel_car_kb)


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
    id = msg.from_user.id
    print(data)
    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    manager_cars.add_end_time(
        sign_number=data["license_plate"],
        id = id,
        time=convert_to_postgresql_datetime(datetime.datetime.now())
    )
    result = manager_cars.deselect_car(data["license_plate"], password=data["password"])
    if result == False:
        await  msg.answer("wrong secret", reply_markup=cancel_car_kb)
    else:
        await  msg.answer("it is all", reply_markup=base_kb)


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

def convert_to_postgresql_datetime(timestamp):
    return datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')