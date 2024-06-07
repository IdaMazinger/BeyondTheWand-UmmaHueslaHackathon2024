import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "64:E8:33:88:51:AE"
DEVICE_NAME = "ESP32-C3-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def listen_to_device():
    async with BleakClient(DEVICE_ADDRESS) as wand:
        x = await wand.is_connected()
        while True:
            value = bytes(await wand.read_gatt_char(CHARACTERISTIC_UUID))
            print(value)
        # for service in wand.services:
        #     if service.uuid == SERVICE_UUID:
        #         print("Service: ", service.uuid, service.description)
        #         for char in service.characteristics:
        #             if char.uuid == CHARACTERISTIC_UUID:
        #
        #                 if "read" in char.properties:
        #                     try:
        #                         value = bytes(await wand.read_gatt_char(char.uuid))
        #                     except Exception as e:
        #                         value = str(e).encode()
        #                 else:
        #                     value = None
        #                 print("characteristics: ", char.uuid, value)


if __name__ == '__main__':
    asyncio.run(listen_to_device())



