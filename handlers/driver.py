import random
import string

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
    await msg.answer("register or login", reply_markup=auth_kb)

@driver_router.message(F.text == "Register")
async def register_driver(msg: Message, state: FSMContext):
    await state.set_state(RegisterUser.name)
    await msg.answer("write name")

@driver_router.message(RegisterUser.name)
async def register_driver_input_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(RegisterUser.surname)
    await msg.answer("write surname")

@driver_router.message(RegisterUser.surname)
async def register_driver_input_surname(msg: Message, state: FSMContext):
    await state.update_data(surname=msg.text)
    await state.set_state(RegisterUser.password)
    await msg.answer("write password")

@driver_router.message(RegisterUser.password)
async def register_driver_input_password(msg: Message, state: FSMContext):
    await state.update_data(password=msg.text)
    data = await state.get_data()
    connect = db.get_connection()
    auth_user = db.AuntithicateUser(connect.connection_db)
    resutl = auth_user.register_user(
        name = data["name"],
        login= data["surname"],
        password=data["password"]
    )
    await  msg.answer(f"вы зареганы:{resutl}", reply_markup=auth_kb)

@driver_router.message(F.text == "Login")
async def driver_login(msg: Message, state: FSMContext):
    await state.set_state(LoginUser.name)
    await msg.answer("write name")
@driver_router.message(LoginUser.name)
async def input_name_login_user(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(LoginUser.password)
    await msg.answer("write password")

@driver_router.message(LoginUser.password)
async def input_password_login_user(msg: Message, state: FSMContext):
    await state.update_data(password=msg.text)
    data = await state.get_data()
    connect = db.get_connection()
    auth_user = db.AuntithicateUser(connect.connection_db)
    result =  auth_user.login_user(
        name=data["name"],
        password=data["password"]
    )
    await  state.clear()
    if result == True:
        await msg.answer("принято", reply_markup=user_kb)
    else:
        await msg.answer("неверные данные", reply_markup=auth_kb)

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
