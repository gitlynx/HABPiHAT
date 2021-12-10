'''
Pressure Sensor module
'''
import time

from threading import Thread
from cmdr import Cmd
from hab_logger import LoggerBase
#from bmp388_sensor import BmpSensor

class Sensor(LoggerBase, Thread):
    ''' Sensor class '''

    def __init__(self):
        Thread.__init__(self, name='Sensor')
        LoggerBase.__init__(self, "SENSOR")
        self._bmp = None
        #self._bmp = BmpSensor()

    @property
    def bmp(self):
        ''' Get bmp sensor instance '''
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
    '''
    Derived command class to access the pressure sensor
    from the command shell
    '''

    def __init__(self, sensor: Sensor) -> None:
        Cmd.__init__(self, 'sensor')
        self._sensor = sensor

    @property
    def bmp(self):
        ''' Get bmp sensor instance '''
        return self._sensor.bmp

    def do_altitude(self, args): # pylint: disable=unused-argument
        """ show altitude in [m] """
        print(f"Altitude: {self.bmp.get_altitude():6.4f} m")

    def do_temperature(self, args): # pylint: disable=unused-argument
        """ show temperature in [°C] """
        print(f"Temperature: {self.bmp.get_temperature():5.2f} °C")

    def do_pressure(self, args): # pylint: disable=unused-argument
        """ show pressure in [hPa] """
        print(f"Pressure: {self.bmp.get_pressure():6.4f} hPa")
