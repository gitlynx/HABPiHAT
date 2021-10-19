from cmdr import Cmd
from hab_logger import LoggerBase
#from bmp388_sensor import BmpSensor

class Sensor(LoggerBase):
    def __init__(self):
        LoggerBase.__init__(self, "SENSOR")
        self._bmp = None
        #self._bmp = BmpSensor()

    @property
    def bmp(self):
        return self._bmp

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