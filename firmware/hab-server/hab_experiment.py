'''
Communication interface with project experiments
'''
import time
from serial import Serial, SerialException
from hab_logger import BaseLogger
from hab_config import HabExperimentConfig as config

class HabExperiment:
    """ Class for serial communication with project experiment """

    def __init__(self, name):
        port = config[name]["PORT"] or "/dev/ttyS0"
        baudrate = config[name]["BAUDRATE"] or 115200
        read_interval = config[name]["READ_INTERVAL"] or 5
        self.logger = BaseLogger(name)
        self.serial = Serial(port, baudrate)
        self.is_enabled = False
        self.read_interval = read_interval
        self.t_start = time.time()
        self.connect()
        self.enable()

    def __del__(self):
        self.close()

    def connect(self):
        """ Open serial port """
        try:
            self.serial.open()
            self.logger.log_info("Connection opened")
        except SerialException:
            pass

    def close(self):
        """ Close serial port """
        self.serial.close()
        self.logger.log_info("Connection closed")

    def _send_command(self, cmd: str):
        """ Send command to serial port """
        if self.serial.is_open:
            data: bytes = cmd.encode('utf-8')
            self.serial.write(data)

    def _read_data(self) -> str:
        """ Read response from serial port """
        return self.serial.readline().decode('utf-8')

    def enable(self):
        """ Send enable command """
        self._send_command("enable")
        response = self._read_data()
        self.is_enabled = response == 'OK'
        self.logger.log_info(f"Enabled: {response}")

    def disable(self):
        """ Send disable command """
        self._send_command("disable")
        response = self._read_data()
        self.is_enabled = not response == 'OK'
        self.logger.log_info(f"Disabled: {response}")

    def reset(self):
        """ Send reset command """
        self._send_command("reset")
        response = self._read_data()
        self.logger.log_info(f"Reset: {response}")

    def do_work(self):
        """ Periodically read data from experiment """
        t_now = time.time()
        if self.is_enabled and t_now - self.t_start > self.read_interval:
            print(self._read_data())
            self.t_start = t_now
