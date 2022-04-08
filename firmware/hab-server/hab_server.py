"""
HAB server application
"""
import socket
import sys
import threading
import time

from hab_experiment import HabExperiment
from hab_logger import BaseLogger
from hab_shell import HabShell
from hab_config import HabShellConfig
from sensor import Sensor, SensorCmd
from hab_gps import Gps, GpsCmd

HOST = HabShellConfig['HOST'] or '0.0.0.0'
PORT = HabShellConfig['PORT'] or 1234

sensor: Sensor = Sensor()
sensor_cmd: SensorCmd = SensorCmd(sensor)
logger: BaseLogger = BaseLogger('Hab server')

gps: Gps = Gps(BaseLogger('GPS'))
gps_cmd: GpsCmd = GpsCmd(gps)

def accept_connection():
    ''' Accept network connections for HAB shell '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    logger.log_info(f"Accepting shell connections on host {HOST}:{PORT}")
    while True:
        client, address = sock.accept()
        client.settimeout(None)
        logger.log_info(f"New connection from {address[0]}:{address[1]}")
        shell = HabShell(client)
        shell.register(sensor_cmd)
        #shell.register(gps_cmd)
        #shell.register(rf_cmd)
        shell.start()

if __name__ == "__main__":
    logger.log_info("Starting HAB server")
    thread = threading.Thread(target=accept_connection, name='accept_connection', daemon=False)
    thread.start()
    sensor.start()
    gps.start()
    #rf.start()
    experiment1 = HabExperiment("EXPERIMENT1")
    experiment2 = HabExperiment("EXPERIMENT2")
    try:
        while True:
            experiment1.do_work()
            experiment2.do_work()
            time.sleep(1)

    except KeyboardInterrupt:
        thread.join()
        sensor.join()
        gps.join()
        experiment1.__del__()
        experiment2.__del__()
        sys.exit(0)
