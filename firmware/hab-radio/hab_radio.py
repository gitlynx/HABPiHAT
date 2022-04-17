from re import I
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
                port=None, 
                baudrate=self.DRA818BAUD,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                rtscts=False,
                dsrdtr=False,
                timeout=0.5)

        self.serial.port = self.port
        self.serial.rts=False
        self.serial.open()

        sleep(0.5)
        
    def __del__(self):
        if self.serial:
            self.serial.close()
            self.serial = None

    def _reopen(self):
        self.serial.close()
        sleep(1)
        self.serial.open()

    def _writeConfig(self, line: bytes):
        # Write command
        for a in range(3):
            self.serial.write(line)
            _response = bytes(self.serial.readline())
            if b"DMOERROR" not in _response:
                print(f"{a}: OK  {line}")
                break
            else:
                print(f"{a}: NOK {line}")
            sleep(1)
        sleep(0.5)

    def PTT(self, enable: bool = False):
        self.serial.rts = enable

    def control(self, enable):
        if enable:
            self.serial.open()
        else:
            self.serial.close()

    def configRadio(self):
        # Reopen
        self._reopen()
        # Connect
        self._writeConfig(b"AT+DMOCONNECT\r\n")
        # Set Volume
        self._writeConfig(b"AT+DMOSETVOLUME=%d\r\n" % (self.VOLUMN))
        # Set filter
        self._writeConfig(b"AT+SETFILTER=0,0,0\r\n")
        # Program Radio
        self._writeConfig(b"AT+DMOSETGROUP=%d,%3.4f,%3.4f,%s,%d,%s\r\n" % (
            self.MODE, 
            self.TXFREQUENCY, 
            self.RXFREQUENCY, 
            self.CTCSS, 
            self.SQUELCH, 
            self.CTCSS))

if __name__ == "__main__":
    radio = DRA818("/dev/ttySC3")

    radio.configRadio()


