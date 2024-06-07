import math
import cv2
import mouse
import asyncio
import numpy as np
from bleak import BleakScanner, BleakClient

DEVICE_ADDRESS = "64:E8:33:88:51:AE"
DEVICE_NAME = "ESP32-C3-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
BUTTON_DOWN = False


def disconnected_callback(client):
    print("Disconnected!")
    exit()


async def listen_to_device():
    async with BleakClient(DEVICE_ADDRESS) as wand:
        # x = await wand.is_connected()
        last_id = -1
        wand_corners = np.float32([[-70, -45], [-165, -45], [-165, 45]])
        screen_corners = np.float32([[0, 0], [1920, 0], [1920, 1080]])
        affine_transformation_matrix = cv2.getAffineTransform(wand_corners, screen_corners)
        print(affine_transformation_matrix)
        while wand.is_connected:
            string_value = bytes(await wand.read_gatt_char(CHARACTERISTIC_UUID))
            string_value = string_value.decode('UTF-8')
            # print(string_value)

            values = string_value.split(",")
            value_id, roll, pitch, yaw, button_state = values  # up and right neg
            if not value_id == last_id:
                button_action(button_state)
                print(pitch, yaw)  # left:-70 right:-165 up:-45 down:45
                mouse_movement = cv2.transform(np.array([np.float32([[float(pitch), float(yaw)]])]), affine_transformation_matrix)[0][0]
                move_mouse(mouse_movement[0], mouse_movement[1])
                # print(last_pitch - pitch)
                last_id = value_id


def button_action(button_down: bool):
    global BUTTON_DOWN
    if button_down != BUTTON_DOWN:
        if button_down:
            mouse.press()
        else:
            mouse.release()

        BUTTON_DOWN = button_down


def move_mouse(x, y):
    mouse.move(x, y, absolute=False, duration=0.1)


if __name__ == '__main__':
    asyncio.run(listen_to_device())

