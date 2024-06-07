import serial


def main():
    wand = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    while True:
        motion = wand.readline()
        print(motion)


def save_motion(data):
    pass


if __name__ == '__main__':
    pass