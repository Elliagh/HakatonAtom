from dataclasses import dataclass

import psycopg2


class ConnectionBaseData:

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        try:
            self.connection_db = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )

            self.connection_db.autocommit = True
        except Exception as _ex:
            print("[INFO] error to connect data base")

    def close_connection(self):
        if self.connection_db:
            self.connection_db.close()


@dataclass
class User:
    name: str
    surname: str


@dataclass
class Car:
    license_plate: str
    model: str
    year_of_realease: str
    mileage: int
    amount_of_fuel: int
    type_of_car: str
    type_of_fuel: str


class ManagerCars:



    def __init__(self, connection):
        self.connection = connection

    def add_new_car(self, car):
        try:
            string_query = f"""INSERT INTO car (license_plate, model, year_of_realease, mileage, amount_of_fuel, type_of_car, type_of_fuel)
                            VALUES('{car.license_plate}', '{car.model}', '{car.year_of_realease}', 
                                    {car.mileage}, {car.amount_of_fuel}, '{car.type_of_car}', '{car.type_of_fuel}');"""
            with self.connection.cursor() as cursor:
                cursor.execute(string_query)
        except Exception as _ex:
            print("[INFO] error to add data car")

    def get_all_cars(self):
        try:
            string_query = "select * from car"
            with self.connection.cursor() as cursor:
                cursor.execute(string_query)
                raw_cars = cursor.fetchall()
                result_cars = []
                for raw_car in raw_cars:
                    result_cars.append(self.convert_tuple_to_car(raw_car))
                return result_cars
        except Exception as _ex:
            print("[INFO] error to get cars")

    def get_info_by_license_plate(self, number_sign):
        try:
            string_query = f"select * from car where license_plate = '{number_sign}'"
            with self.connection.cursor() as cursor:
                cursor.execute(string_query)
                raw_car = cursor.fetchone()
                result_car = self.convert_tuple_to_car(raw_car)
                return result_car
        except Exception as _ex:
            print("[INFO] error find car")

    def update_car(self, car, name_column, new_value):
        string_query = f"""
                update car
                set {name_column} = {new_value}
                where license_plate = '{car.license_plate}'"""
        with self.connection.cursor() as cursor:
            cursor.execute(string_query)

    def check_connection(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select version()")
            print(f"Server version {cursor.fetchone()}")


    def convert_tuple_to_car(self, tuple_car):
        car = Car(
            license_plate=tuple_car[0],
            model=tuple_car[1],
            year_of_realease=tuple_car[2],
            mileage=tuple_car[3],
            amount_of_fuel=tuple_car[4],
            type_of_car=tuple_car[5],
            type_of_fuel=tuple_car[6]
        )
        return car


