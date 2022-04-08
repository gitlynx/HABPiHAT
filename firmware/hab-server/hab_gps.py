'''
GPS module
'''
import time

from threading import Thread
from cmdr import Cmd
from gpsdclient import GPSDClient
from hab_logger import BaseLogger

class Gps(Thread):
    ''' GPS class '''

    def __init__(self, logger: BaseLogger):
        Thread.__init__(self, name='GPS')
        self._gps = GPSDClient(host="127.0.0.1")
        self._log = logger
        self._lat = 0.0
        self._lon = 0.0

    @property
    def longitude(self):
        ''' Get longitude '''
        return self._lon

    @property
    def latitude(self):
        ''' Get latitude '''
        return self._lat

    def run(self) -> None:
        self._log.log_info("GPS logging started")
        while True:
            for result in self._gps.dict_stream(convert_datetime=True):
                if result["class"] == "TPV":
                    self._lat = result.get("lat", "n/a")
                    self._lon = result.get("lon", "n/a")
                    self._log.log_info(f"Lat: {self._lat}")
                    self._log.log_info(f"Lon: {self._lon}")
                    time.sleep(10)

class GpsCmd(Cmd):
    '''
    Access GPS data from the command shell
    '''

    def __init__(self, gps: Gps) -> None:
        Cmd.__init__(self, 'gps')
        self._gps = gps

    def do_latitude(self, args):
        """ show latitude """
        print(f"Latitude: {self._gps.latitude}")

    def do_longitude(self, args):
        """ show longitude """
        print(f"Longitude: {self._gps.longitude}")
