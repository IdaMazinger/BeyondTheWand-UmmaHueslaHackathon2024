import math
from datetime import datetime
from time import time
import os
import cv2
import mouse
import asyncio
import numpy as np
import pandas as pd
from bleak import BleakScanner, BleakClient

DEVICE_ADDRESS = "64:E8:33:88:51:AE"
DEVICE_NAME = "ESP32-C3-BLE"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


def disconnected_callback(client):
    print("Disconnected!")
    exit()


async def learn_gestures():
    async with (BleakClient(DEVICE_ADDRESS)) as wand:
        header = ["delta_time", "roll", "pitch", "yaw", "label"]
        last_id = -1
        while wand.is_connected:
            gesture_type = input("Gesture type? (g=gesture, r or enter=random, e=exit) ")

            if gesture_type == "e":
                await wand.disconnect()
                exit()
            label = "gesture" if gesture_type == "g" else "random"

            start_datetime = datetime.now()
            string_start_time = str(start_datetime.year) + "-" + str(start_datetime.month) + "-" + str(start_datetime.day) + "-" + str(start_datetime.hour) + "-" + str(start_datetime.minute) + "-" + str(start_datetime.second)
            file_name = string_start_time + ".csv"
            file_path = 'training_data/'
            data = []

            button_state = False
            while button_state == False:
                string_value = bytes(await wand.read_gatt_char(CHARACTERISTIC_UUID))
                string_value = string_value.decode('UTF-8')
                values = string_value.split(",")
                value_id, roll, pitch, yaw, button_value = values
                button_state = False if button_value == "0" else True

            start_time = int(time() * 1000)
            while button_state == True:
                string_value = bytes(await wand.read_gatt_char(CHARACTERISTIC_UUID))
                string_value = string_value.decode('UTF-8')
                values = string_value.split(",")
                value_id, roll, pitch, yaw, button_value = values
                button_state = False if button_value == "0" else True

                if not value_id == last_id and button_state:
                    delta_time = (time() * 1000) - start_time
                    roll, pitch, yaw = round(float(roll), 1), round(float(pitch), 1), round(float(yaw), 1)
                    data.append([delta_time, roll, pitch, yaw, label])

            df = pd.DataFrame(data, columns=header)
            df.to_csv(file_path + file_name, index=False)


if __name__ == '__main__':
    asyncio.run(learn_gestures())

