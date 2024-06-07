import mouse
import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_ADDRESS = "64:E8:33:88:51:AE"
DEVICE_NAME = "ESP32-C3-BLE"


async def get_device() -> BleakClient:
    devices = await BleakScanner.discover()
    for d in devices:
        if d.address == DEVICE_ADDRESS and d.name == DEVICE_NAME:
            return BleakClient(d)


async def listen_to_device():
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



def move_mouse(x, y):
    mouse.move(x, y, absolute=False, duration=0.1)


def test_mouse():
    while True:
        x = input("x: ")
        y = input("y: ")
        move_mouse(x, y)


if __name__ == '__main__':
    # test_mouse()
    # device = asyncio.run(get_device())
    asyncio.run(listen_to_device())

