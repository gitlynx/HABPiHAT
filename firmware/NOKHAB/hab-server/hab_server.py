from os import name
import socket
import sys
import threading

from hab_prompt import HabPrompt
from sensor import Sensor, SensorCmd
from threading import Thread

HOST = '0.0.0.0'
PORT = 1234

sensor: Sensor = Sensor()
sensor_cmd: SensorCmd = SensorCmd(sensor)

def accept_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        client, address = s.accept()
        client.settimeout(None)
        p = HabPrompt(client)
        p.register(sensor_cmd)
        p.start()

if __name__ == "__main__":
    thread = threading.Thread(target=accept_connection, name='accept_connection', daemon=False)
    thread.start()
    sensor.start()
    try:
        thread.join()
        sensor.join()
    except KeyboardInterrupt:
        sys.exit(0)