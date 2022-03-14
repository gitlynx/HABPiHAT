###############################################################################
#
# Base Python Module for working with Serial ports
#
###############################################################################
import pynmea2
import serial
import io

class PortSettings:


    def __init__(self, *args, **kwargs):
        self.baud = None
        self.dev = None

        for key, value in kwargs.items():
            print ("key: {}, value: {}".format(key, value))
            if key == 'baudrate':
                self.baud = value
            if key == 'device':
                self.dev = value

    @property
    def device(self):
        return self.dev

    @property
    def baudrate(self):
        return self.baud


class ParserBase:
    def __init__(self):
        pass


class SerialBase:
    def __init__(self, *args, **kwargs):
#        for key, value in kwargs.items():
#            if 'settings' = key:
#                self.settings = PortSettings(*args, **kwargs)
        pass


class ParseGps:
    def getAltitude(self, str):
        msg = pynmea2.parse(str)
        return msg.altitude

    @staticmethod
    def getTimeStamp():
        msg = pynmea2.parse(str)
        return msg.timestamp


class GPSData:
    def __init__(self):
        self.string = None

    def set

def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print("Timestamp: {} -- Lat: {} {} -- Lon: {} {} -- Altitude: {} {} -- Satellites: {}".format(msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats))


# Module Unit test #
# ################ #

if __name__ == "__main__":
    settings = PortSettings(baudrate='9600', device='/dev/ttyACM0')
    print("Settings: {}, {}".format(settings.baudrate, settings.device))

    ser = serial.Serial(settings.device, settings.baudrate, timeout=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    while(True):
        line =  sio.readline()
        print("Line: {}".format(line))
        parseGPS(line)