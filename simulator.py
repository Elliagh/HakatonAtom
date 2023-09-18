import asyncio
import random
from typing import List

import can
from can.notifier import MessageRecipient


current_engine_rpm = 2000
current_vehicle_speed = 40

def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(msg)

async def send_vehicle_data(bus):
    global current_engine_rpm, current_vehicle_speed

    # Генерируем случайное изменение состояния машины
    delta_engine_rpm = random.randint(-50, 50)
    delta_vehicle_speed = random.uniform(-5, 5)
    delta_vehicle_fuel = random.uniform(0, 0.3)
    # ...

    # Обновляем значения состояния машины с плавным изменением
    current_engine_rpm += delta_engine_rpm
    current_vehicle_speed += delta_vehicle_speed

    # Проверяем максимальную скорость автомобиля
    if current_vehicle_speed > 60:
        current_vehicle_speed = 60
    elif current_vehicle_speed < 40:
        current_vehicle_speed = 40

    # Определяем PGN (Parameter Group Number) для отправки данных
    pgn = 0x1234  # Замените на соответствующий PGN

    # Формируем сообщение для отправки
    message = can.Message(arbitration_id=pgn, data=bytearray([int(current_vehicle_speed), 3]))

    # Отправляем сообщение
    bus.send(message)


async def main() -> None:
    """The main function that runs in the loop."""

    with can.Bus(
        interface="virtual", channel="my_channel_0", receive_own_messages=True
    ) as bus:
        reader = can.AsyncBufferedReader()
        logger = can.Logger("logfile.asc")

        listeners: List[MessageRecipient] = [
            print_message,  # Callback function
            reader,  # AsyncBufferedReader() listener
            logger,  # Regular Listener object
        ]
        # Create Notifier with an explicit loop to use for scheduling of callbacks
        loop = asyncio.get_running_loop()
        notifier = can.Notifier(bus, listeners, loop=loop)
        # Start sending first message
        
        while True:

            await send_vehicle_data(bus)

            await asyncio.sleep(0.5)

            message = await reader.get_message()

        # Wait for last message to arrive
        await reader.get_message()
        print("Done!")

        # Clean-up
        notifier.stop()


if __name__ == "__main__":
    asyncio.run(main())