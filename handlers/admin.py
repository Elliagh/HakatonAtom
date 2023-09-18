from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, F, Router
from aiogram.types import Message

from kb import admin_kb, change_info_kb, base_kb, cancel_kb
from db import ManagerCars
from db import Car
import db

admin_router = Router()


class AddCar(StatesGroup):
    license_plate = State()
    car_model = State()
    year_of_release = State()
    mileage = State()
    amount_of_fuel = State()
    type_of_car = State()
    type_of_fuel = State()

class ChangeCarInfo(StatesGroup):
    car_license_plate = State()
    car_property = State()
    car_new_value = State()

class DeleteCar(StatesGroup):
    car_license_plate = State()

@admin_router.message(F.text == "Admin")
async def admin_menu(msg: Message):

    await msg.answer("Что хотите сделать", reply_markup=admin_kb)

# Cancel

@admin_router.message(F.text == "Отмена")
async def cancel_action(msg: Message, state: FSMContext):
    await state.clear()

    await msg.answer("Действие отменено", reply_markup=admin_kb)

@admin_router.message(F.text == "Back to base menu")
async def back_to_menu(msg: Message):

    await msg.answer("Возврат в главное меню", reply_markup=base_kb)

# Add Car FSM

@admin_router.message(F.text == "Add new car")
async def start_add_car(msg: Message, state: FSMContext):
    await state.set_state(AddCar.license_plate)
    await msg.answer("Напиши номерной знак машины", reply_markup=cancel_kb)

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
        [KeyboardButton(text="Доставка")],
        [KeyboardButton(text="Отмена")]
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
        [KeyboardButton(text="АИ-100")],
        [KeyboardButton(text="Отмена")]
    ]

    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await msg.answer("Выбери тип топлива", reply_markup=kb)

@admin_router.message(AddCar.type_of_fuel)
async def process_type_of_fuel(msg: Message, state: FSMContext):
    await state.update_data(type_of_fuel=msg.text)
    data = await state.get_data()
    await state.clear()
    
    new_car = Car(
        license_plate=data["license_plate"],
        model=data["car_model"],
        year_of_release=data["year_of_release"],
        mileage=data["mileage"],
        amount_of_fuel=data["amount_of_fuel"],
        type_of_fuel=data["type_of_fuel"],
        type_of_car=data["type_of_car"],
        busy=False,
        temp_sign="1234"
    )
    connect = db.get_connection()
    print(new_car)
    manager_cars = db.ManagerCars(connect.connection_db)
    manager_cars.add_new_car(new_car)

    await msg.answer("Машина добавлена в базу данных", reply_markup=base_kb)


# Change Info FSM

@admin_router.message(F.text == "Change car info")
async def start_change_info(msg: Message, state: FSMContext):
    await state.set_state(ChangeCarInfo.car_license_plate)
    await msg.answer("Напиши номерной знак машины, у которой вы хотите поменять имнформацию", reply_markup=cancel_kb)


@admin_router.message(ChangeCarInfo.car_license_plate)
async def process_license_plate(msg: Message, state: FSMContext):
    await state.update_data(license_plate=msg.text)
    await state.set_state(ChangeCarInfo.car_property)

    await msg.answer("Выбери что хочешь изменить", reply_markup=change_info_kb)

@admin_router.message(ChangeCarInfo.car_property)
async def process_car_property(msg: Message, state: FSMContext):
    await state.update_data(car_property=msg.text)
    await state.set_state(ChangeCarInfo.car_new_value)

    await msg.answer("Напиши новое значение", reply_markup=cancel_kb)

@admin_router.message(ChangeCarInfo.car_new_value)
async def process_new_value(msg: Message, state: FSMContext):
    await state.update_data(new_value=msg.text)
    data = await state.get_data()
    await state.clear()

    license_plate_car = data["license_plate"]
    car_property = data["car_property"]
    new_value = data["new_value"]

    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    find_car = manager_cars.get_info_by_license_plate(license_plate_car)

    if car_property == "mileage" or car_property == "amount_of_fuel":
        pass
    else:
        new_value = "'" + new_value + "'"
    manager_cars.update_car(
        find_car,
        car_property,
        new_value
    )

    print(data)

    await msg.answer("Информация успешно обновлена", reply_markup=admin_kb)

# Delete Car Info

@admin_router.message(F.text == "Delete car")
async def start_delete_car(msg: Message, state: FSMContext):
    await state.set_state(DeleteCar.car_license_plate)

    await msg.answer("Напиши номерной знак машины", reply_markup=cancel_kb)

@admin_router.message(DeleteCar.car_license_plate)
async def process_license_plate(msg: Message, state: FSMContext):
    await state.update_data(license_plate=msg.text)
    license_plate = await state.get_data()

    connect = db.get_connection()
    manager_cars = db.ManagerCars(connect.connection_db)
    manager_cars.delete_car(license_plate["license_plate"])

    await msg.answer("Машина удалена из базы данных", reply_markup=admin_kb)

