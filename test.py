import asyncio

import mouse
from bleak import BleakClient, BleakScanner

DEVICE_ADDRESS = "64:E8:33:88:51:AE"
DEVICE_NAME = "ESP32-C3-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


def disconnected_callback(client):
    print("Disconnected!")
    exit()


async def listen_to_device():
    async with BleakClient(DEVICE_ADDRESS, disconnected_callback=disconnected_callback) as wand:
        # x = await wand.is_connected()
        last_id = -1
        while wand.is_connected:
            string_value = bytes(await wand.read_gatt_char(CHARACTERISTIC_UUID))
            string_value = string_value[1::]
            print(string_value)

            values = string_value.split(",")
            value_id, ax, ay, az, gx, gy, gz, button_state = values[0]
            if not value_id == last_id:
                print(gx, gy)


async def check_device_serices():
    async with BleakClient(DEVICE_ADDRESS) as wand:
        x = await wand.is_connected()
        for service in wand.services:
            print("Service: ", service.uuid, service.description)
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await wand.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                print("characteristics: ", char.uuid, value)


async def get_device() -> BleakClient:
    devices = await BleakScanner.discover()
    for d in devices:
        print(d.name, d.address)
        if d.address == DEVICE_ADDRESS and d.name == DEVICE_NAME:
            return BleakClient(d)


def test_mouse():
    while True:
        x = input("x: ")
        y = input("y: ")
        move_mouse(x, y)


def move_mouse(x, y):
    mouse.move(x, y, absolute=False, duration=0.1)


if __name__ == '__main__':
    # asyncio.run(get_device())
    asyncio.run(listen_to_device())
