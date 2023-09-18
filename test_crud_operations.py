import json
import db as mc


def add_two_cars():
    connection = mc.get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    manager_cars.check_connection()

    new_car = mc.Car(
        "AOAfda",
        "gas",
        "2002-05-05",
        "2000",
        "300",
        "carshering",
        "dizel"
    )

    manager_cars.add_new_car(new_car)

    second_car = mc.Car(
        'fdasf',
        'gas',
        '2002-05-05',
        '2000',
        '300',
        'Каршеринг',
        'ai-80'
    )
    manager_cars.add_new_car(second_car)


def print_all_cars():
    connection = mc.get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    cars = manager_cars.get_all_cars()
    print(cars)
    return cars

def find_car_by_number_sign(number_sign):
    connection = mc.get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    car = manager_cars.get_info_by_license_plate(number_sign)
    print(car)
    return car

def update_car(car, name_column, new_value):
    connection = mc.get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    manager_cars.update_car(car, name_column, new_value)

def calculate_cost_usage_car(car):
    connection = mc.get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    cost = manager_cars.cost_usage(car)
    print(cost)
    return cost

add_two_cars()
print_all_cars()
find_car = find_car_by_number_sign("fdasf")
update_car(find_car, "model", "'sedan'")
find_car = find_car_by_number_sign("fdasf")
calculate_cost_usage_car(find_car)