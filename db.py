import asyncio

import asyncpg

async def add_new_car(car_info: dict):
    
    conn = await asyncpg.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="12345678",
        port=5432
    )

    get_drivers_query = "SELECT * FROM driver"

    result = await conn.fetch(get_drivers_query)
    
    await conn.close()

async def change_car_info(info_to_change: dict):
    pass

async def delete_car(license_plate: str):
    pass

asyncio.run(add_new_car({"1":1}))

