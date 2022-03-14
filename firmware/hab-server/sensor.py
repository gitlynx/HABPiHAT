'''
Pressure Sensor module
'''
import time

from threading import Thread
from cmdr import Cmd
from hab_logger import BaseLogger
#from bmp388_sensor import BmpSensor

class Sensor(BaseLogger, Thread):
    ''' Sensor class '''

    def __init__(self):
        Thread.__init__(self, name='Sensor')
        BaseLogger.__init__(self, "Sensor")
        self._bmp = None
        #self._bmp = BmpSensor()
        self._altitude = 0
        self._temperature = 0
        self._pressure = 0

    @property
    def altitude(self):
        ''' Get altitude '''
        return self._altitude

    @property
    def temperature(self):
        ''' Get temperature '''
        return self._temperature

    @property
    def pressure(self):
        ''' Get pressure '''
        return self._pressure

    def _log_data(self):
        self.log_info("Alt: ")
        self.log_info("Temp: ")
        self.log_info("Pressure: ")
        #self._altitude = self._bmp.get_altitude()
        #self.log_info(f"Alt: {self._altitude}")

    def run(self) -> None:
        self.log_info("Sensor logging started")
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

    def do_altitude(self, args): # pylint: disable=unused-argument
        """ show altitude in [m] """
        print(f"Altitude: {self._sensor.altitude:6.4f} m")

    def do_temperature(self, args): # pylint: disable=unused-argument
        """ show temperature in [°C] """
        print(f"Temperature: {self._sensor.temperature:5.2f} °C")

    def do_pressure(self, args): # pylint: disable=unused-argument
        """ show pressure in [hPa] """
        print(f"Pressure: {self._sensor.pressure:6.4f} hPa")
