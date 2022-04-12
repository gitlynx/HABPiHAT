import serial
from time import sleep

class DRA818():
    DRA818BAUD=9600
    _VOLUME=7
    TXFREQUENCY = 144.400
    RXFREQUENCY = 145.825
    MODE = 0 # 1 = FM (supposedly 5kHz deviation), 0 = NFM (2.5 kHz Deviation)
    SQUELCH = 0 # Squelch Value, 0-8
    CTCSS = b'0000'
    VOLUMN = 7

    def __init__(self, port: str):
        self.port = port
        self.serial = serial.Serial(
                port=port, 
                baudrate=self.DRA818BAUD,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.5)
        
    def __del__(self):
        if self.serial:
            self.serial.close()
            self.serial = None

    def configRadio(self):

        # Connect
        self.serial.write(b"AT+DMOCONNECT\r\n") 
        _response = bytes(self.serial.readline())
        print(f"Connect: {_response}")

        # Set Volume
        self.serial.write(b"AT+DMOSETVOLUME=%d\r\n" % (self.VOLUMN))
        _response = self.serial.readline()
        print(f"Volume: {_response}")

        # Set filter
        self.serial.write(b"AT+SETFILTER=0,0,0\r\n")
        _response = self.serial.readline()
        print(f"Filter: {_response}")

        # Program Radio
        self.serial.write(b"AT+DMOSETGROUP=%d,%3.4f,%3.4f,%s,%d,%s\r\n" % (
            self.MODE, 
            self.TXFREQUENCY, 
            self.RXFREQUENCY, 
            self.CTCSS, 
            self.SQUELCH, 
            self.CTCSS))
        _response = self.serial.readline()
        print(f"Program: {_response}")


if __name__ == "__main__":
    radio = DRA818("/dev/ttySC3")

    radio.configRadio()


