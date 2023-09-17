import json
import db as mc


def get_connection():
    with open('ConnectionInfo.json', 'r') as connection_json:
        connection_data = json.load(connection_json)
        connection = mc.ConnectionBaseData(
            host=connection_data["host"],
            user=connection_data["user"],
            password=connection_data["password"],
            db_name=connection_data["db_name"]
        )
        return connection

def add_two_cars():
    connection = get_connection()
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

    manager_cars.add_new_car(new_car);

    second_car = mc.Car(
        "fdasf",
        "gas",
        "2002-05-05",
        "2000",
        "300",
        "carshering",
        "dizel"
    )
    manager_cars.add_new_car(second_car)


def print_all_cars():
    connection = get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    cars = manager_cars.get_all_cars()
    print(cars)

def find_car_by_number_sign(number_sign):
    connection = get_connection()
    manager_cars = mc.ManagerCars(connection.connection_db)
    car = manager_cars.get_info_by_license_plate(number_sign)
    print(car)



add_two_cars()
print_all_cars()
find_car_by_number_sign("fdasf")
