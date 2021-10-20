from os import name
import socket
import sys
import threading

from hab_logger import LoggerBase
from hab_shell import HabShell
from sensor import Sensor, SensorCmd
from threading import Thread

HOST = '0.0.0.0'
PORT = 1234

sensor: Sensor = Sensor()
sensor_cmd: SensorCmd = SensorCmd(sensor)
logger: LoggerBase = LoggerBase('SERVER')

def accept_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    logger.info(f"Accepting shell connections on host {HOST}:{PORT}")
    while True:
        client, address = s.accept()
        client.settimeout(None)
        logger.info(f"New connection from {address[0]}:{address[1]}")
        shell = HabShell(client)
        shell.register(sensor_cmd)
        #shell.register(gps_cmd)
        #shell.register(rf_cmd)
        shell.start()

if __name__ == "__main__":
    logger.info("Starting HAB server")
    thread = threading.Thread(target=accept_connection, name='accept_connection', daemon=False)
    thread.start()
    sensor.start()
    #gps.start()
    #rf.start()
    try:
        thread.join()
        sensor.join()
    except KeyboardInterrupt:
        sys.exit(0)