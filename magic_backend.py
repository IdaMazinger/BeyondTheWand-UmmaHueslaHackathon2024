import collections
import cv2
import mouse
import asyncio
import numpy as np
from bleak import BleakClient
from time import time
from tensorflow import keras

DEVICE_ADDRESS = "64:E8:33:88:51:AE"
DEVICE_NAME = "ESP32-C3-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
BUTTON_DOWN: bool = False
BUTTON_DOWN_COUNTER: int = 0
# GESTURES = collections.deque(maxlen=20)
# for i in range(20):
#     GESTURES.append([time() * 1000, 0.0, 0.0, 0.0])
# MODEL = keras.models.load_model('wand_gesture1.keras')


def disconnected_callback(client):
    print("Disconnected!")
    exit()


async def listen_to_device():
    async with BleakClient(DEVICE_ADDRESS) as wand:
        last_id = -1
        wand_corners = np.float32([[50, -40], [-50, -40], [-50, 40]])
        screen_corners = np.float32([[0, 0], [1920 * 0.667, 0], [1920 * 0.667, 1080 * 0.667]])
        affine_transformation_matrix = cv2.getAffineTransform(wand_corners, screen_corners)
        mouse_initial_position = cv2.transform(np.array([np.float32([[float(0), float(0)]])]),
                                       affine_transformation_matrix)[0][0]
        move_mouse(mouse_initial_position[0], mouse_initial_position[1])
        # print(affine_transformation_matrix)
        while wand.is_connected:
            string_value = bytes(await wand.read_gatt_char(CHARACTERISTIC_UUID))
            string_value = string_value.decode('UTF-8')
            values = string_value.split(",")

            value_id, roll, pitch, yaw, button_value = values
            button_state = False if button_value == "0" else True
            if not value_id == last_id:
                button_action(bool(button_state))
                if not BUTTON_DOWN or BUTTON_DOWN_COUNTER > 3:
                    roll, pitch, yaw = float(roll), float(pitch), float(yaw)
                    mouse_movement = cv2.transform(np.array([np.float32([[round(yaw, 1), round(pitch, 1)]])]),
                                                   affine_transformation_matrix)[0][0]
                    move_mouse(mouse_movement[0], mouse_movement[1])
                    last_id = value_id
                    # GESTURES.popleft()
                    # GESTURES.append([time() * 1000, roll, pitch, yaw])
                    # analyze_gesture()


def button_action(button_down: bool):
    global BUTTON_DOWN, BUTTON_DOWN_COUNTER
    if button_down:
        BUTTON_DOWN_COUNTER += 1

    if button_down != BUTTON_DOWN:
        if button_down:
            mouse.press()
        else:
            mouse.release()
            BUTTON_DOWN_COUNTER = 0

        BUTTON_DOWN = button_down


def move_mouse(x, y):
    mouse.move(x, y, absolute=True, duration=0.05)


def analyze_gesture():
    first_gesture_time = GESTURES[0][0]
    gestures_deltatime = []
    for gesture in GESTURES:
        gestures_deltatime.append(np.array([gesture[0] - first_gesture_time, gesture[1], gesture[2], gesture[3]]))
    result = MODEL.predict(np.array(gestures_deltatime).reshape(-1, 20 * 4), verbose=0)
    if result[0][0] > 0.1:
        print(result[0][0])


if __name__ == '__main__':
    asyncio.run(listen_to_device())

