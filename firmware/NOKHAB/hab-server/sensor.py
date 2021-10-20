import time

from cmdr import Cmd
from hab_logger import LoggerBase
#from bmp388_sensor import BmpSensor
from threading import Thread

class Sensor(LoggerBase, Thread):
    def __init__(self):
        Thread.__init__(self, name='Sensor')
        LoggerBase.__init__(self, "SENSOR")
        self._bmp = None
        #self._bmp = BmpSensor()

    @property
    def bmp(self):
        return self._bmp

    def _log_data(self):
        self.info("Alt: ")
        self.info("Temp: ")
        self.info("Pressure: ")
        #self.info(f"Alt: {self.bmp.get_altitude()}")

    def run(self) -> None:
        self.info("Sensor logging started")
        while True:
            self._log_data()
            time.sleep(10)

class SensorCmd(Cmd):

    def __init__(self, sensor: Sensor) -> None:
        Cmd.__init__(self, 'sensor')
        self._sensor = sensor

    @property
    def bmp(self):
        return self._sensor.bmp

    def do_altitude(self, args):
        """ show altitude in [m] """
        print("Altitude: {:6.4f} m".format(self.bmp.get_altitude()))

    def do_temperature(self, args):
        """ show temperature in [°C] """
        print("Temperature: {:5.2f} °C".format(self.bmp.get_temperature()))

    def do_pressure(self, args):
        """ show pressure in [hPa] """
        print("Pressure: {:6.4f} hPa".format(self.bmp.get_pressure()))