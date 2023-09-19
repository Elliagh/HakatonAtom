import asyncio
import random
from typing import List
import struct

import can
from can.notifier import MessageRecipient


ENGINE_PGN = 0xF004
DISPLAY_PGN = 0xFEFC

class SimulationManager():

    def __init__(self) -> None:
        self.active_simulations_list = {}

    async def add_simulation(self, driver_id: int, simulation):
        self.active_simulations_list[driver_id] = simulation

        await simulation.run_simulation()

    async def get_simulation_info(self, driver_id: int):
        pass

    async def stop_simulation(self, driver_id):
        sim = self.active_simulations_list[driver_id]

        sim.is_running_simulation = False


class Simulation():

    def __init__(self, simulation_number, fuel_level) -> None:
        self.is_running_simulation = True
        
        self.simulaiton_number = simulation_number
        self.fuel = fuel_level
        self.car_speed = 40

        self.bus = can.Bus(interface="virtual", channel="can0", receive_own_messages=True)
        self.reader = can.AsyncBufferedReader()

        self.listeners: List[MessageRecipient] = [
            self.on_message,  # Callback function
            self.reader,  # AsyncBufferedReader() listener
        ]

        loop = asyncio.get_event_loop()
        self.notifier = can.Notifier(self.bus, self.listeners, loop=loop)

    async def on_message(self, msg):
        # Printe incoming messages in console
        await self.update_info(msg)

        print(msg)

    async def update_info(self, msg: can.Message):

        if msg.arbitration_id == ENGINE_PGN:
            
            encoded_data = bytes(msg.data)

            engine_decoded_data = struct.unpack("IBBHBIB", encoded_data)

            self.car_speed = engine_decoded_data[3] # Скорость

        elif msg.arbitration_id == DISPLAY_PGN:

            encoded_data = bytes(msg.data)

            display_decoded_data = struct.unpack("BBBBH", encoded_data)

            self.car_speed = display_decoded_data[1] # Топливо
    
    async def run_simulation(self):
        
        while self.is_running_simulation:
            await self.write_info_from_display()
            await self.write_info_from_engine()

            await asyncio.sleep(0.5)

        self.notifier.stop()
        self.bus.shutdown()

    async def return_info_to_manager(self):
        data = {'fuel': self.fuel,
                'car_speed': self.car_speed}
        
        return data
        
    async def write_info_from_engine(self):
        
        pgn = ENGINE_PGN

        delta_vehicle_speed = int(random.uniform(-5, 5))

        self.car_speed += delta_vehicle_speed

        if self.car_speed > 60:
            self.car_speed = 60
        elif self.car_speed < 40:
            self.car_speed = 40

        
        data = [
            0, #  Engine Torque Mode
            0, # Driver's Demand Engine - Percent Torque
            0, # Actual Engine - Percent Torque
            self.car_speed, # Engine Speed
            0, # Source Address of Controlling Device for Engine Control
            0, # Engine Starter Mode
            0, # Engine Demand - Percent Torque
        ]

        encoded_data = struct.pack("IBBHBIB", *data)

        #Placeholder
        message = can.Message(arbitration_id=pgn, data=encoded_data)

        self.bus.send(message)

    async def write_info_from_display(self):
        
        # Определяем PGN (Parameter Group Number) для отправки данных
        pgn = DISPLAY_PGN

        chance_to_change_fuel = random.randint(1, 20)

        if chance_to_change_fuel == 3:
            self.fuel -= 1

        if self.fuel < 20:
            self.fuel = 20

        
        data = [
            0, # Washer fluid level
            self.fuel, # Fuel Level
            0, # Fuel Filter Differential Pressure
            0, # Engine Oil Filter Differential Pressure
            0, # Cargo Ambient Temperature
        ]

        encoded_data = struct.pack("BBBBH", *data)

        #Placeholder
        message = can.Message(arbitration_id=pgn, data=encoded_data)

        self.bus.send(message)
        
    

def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(msg.data)


sim_manager = SimulationManager()