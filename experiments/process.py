# Test program for subprocesses
import sys
from os.path import exists
from time import time, sleep
import subprocess

class SSTV:
    INIT=0
    CAPTURE=1
    CAPTURING=2
    TRANSMIT=3
    TRANSMITTING=4
    IDLE=99
    UNKNOWN=-1

    TIMEOUT_CAPTURE = 40
    TIMEOUT_TRANSMIT = 60

    def __init__(self, radio=None):
        self.state = self.IDLE
        self.radio = radio
        self.subproc = None
        self._timeout = None
        self._altitude = "undefined"

    def _subprocess_cleanup(self):
        if self.subproc is not None:
            self.subproc.kill()

    def _subprocess_poll(self):
        """
            check suprocess
            @return True subprocess done
                    False subprocess busy
                    None subprocess error
        """
        self.subproc.poll()
        return self.subproc.returncode

    def _subprocess_spawn(self, process_cmd):
        self.subproc = subprocess.Popen(process_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

    def _radio_enable(self, enable: bool):
        if self.radio is not None:
            self.radio.control(enable)

    def _radio_PTT(self, transmit: bool):
        if self.radio is not None:
            self.radio.PTT(transmit)
            sleep(0.1)

    def _restart(self):
        self.state = self.CAPTURE

    def abort(self):
        self._subprocess_cleanup()
        self.state = self.IDLE

    def _get_altitude(self):
        return self._altitude

    def _set_altitude(self, altitude: str):
        self._altitude = altitude

    altitude = property(fget=_get_altitude, fset=_set_altitude)

    def is_busy(self):
        return(self.state != self.IDLE)

    def run(self, restart: bool = False) -> bool:
        """
            Main runner. 

            @param restart: reset state machine and restart from the beginning
            @return done: true, false
        """
        saved_state = self.state

        if restart:
            self.state = self.CAPTURE

        # State machine
        if self.state == self.IDLE:
            pass

        elif self.state == self.CAPTURE:

            # Start CAPTURE
            self._subprocess_cleanup()
            self._subprocess_spawn(["./capture.sh", self.altitude])
            self._timeout = time() + self.TIMEOUT_CAPTURE
            self.state = self.CAPTURING

        elif self.state == self.CAPTURING:

            # Poll if captureing is (still) in progress
            if self._subprocess_poll() == 0:

                # Conversion completed
                self.state = self.TRANSMIT
            elif time() > self._timeout:

                # Timeout occurred
                self._subprocess_cleanup()
                self.state = self.IDLE
        elif self.state == self.TRANSMIT:
            WAVE_FILE = "/tmp/latest.wav"
            if exists(WAVE_FILE):
                # Open port; Set to transmit
                self._radio_enable(True)
                self._radio_PTT(True)
                self._subprocess_cleanup()
                self._subprocess_spawn(["aplay", WAVE_FILE])
                self.state = self.TRANSMITTING
                self._timeout = time() + self.TIMEOUT_TRANSMIT
            else:
                self.state = self.IDLE

        elif self.state == self.TRANSMITTING:
            if self._subprocess_poll() == 0:

                # Transmit complete
                self._radio_PTT(False)
                self._radio_enable(False)
                self.state = self.IDLE
            elif time() > self._timeout:

                # Timout occurred
                self._radio_PTT(False)
                self._radio_enable(False)
                self._subprocess_cleanup()
                self.state = self.IDLE

        else:
            self.state = self.IDLE


if __name__ == "__main__":
    sstv = SSTV()

    for i in range (400):
        if i == 1:
            sstv.altitude = "1000"
            sstv.run(True)
        else:
            sstv.run()

        if sstv.is_busy():
            print("+", end="")
        else:
            print("-", end="")
        sys.stdout.flush()
        sleep(0.2)

    print("")
