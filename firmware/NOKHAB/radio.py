
import serial

class Radio:
    def __init__(self):
        pass

    def checkConnection(self):
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
        ser.write('AT+DMOCONNECT\r\n')
        line = ser.readline()
        print("{}".format(line))

    def scanFrequency(self, freq):
        cmd = "S+" + freq + '\r\n'
        print ("Scanning frequency: {}".format(cmd))

        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
        ser.write(cmd)
        line = ser.readline()
        print("{}".format(line))


if __name__ == "__main__":
    RF = Radio()
    RF.checkConnection()
#    RF.scanFrequency("150.0000")
    RF.scanFrequency("438.4750")
