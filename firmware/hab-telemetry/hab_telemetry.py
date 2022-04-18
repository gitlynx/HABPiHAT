# Test program for subprocesses
import helpers.serial_interface as ser_io
import helpers.direwolf_interface as direwolf_io
from helpers.hab_radio import DRA818
import sys
from os.path import exists
from time import time, sleep
import subprocess
import os

# CONFIG PART
DEBUG = True
SSID_FROM="ON4NOK-11"
SSID_TO="ON6KX"

DATA_DEVICE = "/dev/ttySC2"
RADIO_DEVICE = "/dev/ttySC3"
BAUD = "115200"

TELEMETRY_DURATION = 1 # in minutes

# CODE PART
# Do Not Change Anything below this line

class Telemetry:
    INIT=0
    CAPTURE=1
    CAPTURING=2
    TRANSMIT=3
    TRANSMITTING=4
    TELEMETRY_SETUP=5
    TELEMETRY_CONNECTING=6
    TELEMETRY_CONNECTED=7
    TELEMETRY_BREAKDOWN=8
    RESTART=90
    SSTV_IDLE=95
    TELEMETRY_IDLE=99
    UNKNOWN=-1

    TIMEOUT_CAPTURE = 40
    TIMEOUT_TRANSMIT = 60

    TELEMETRY_TIMEOUT = 15
    TELEMETRY_DUMMY="0,0,0,0,0,0,0,0"

    def dbg_print(self, line: str):
        if DEBUG:
            print(line)

    def dbg_state_change(self, saved_state):
        if saved_state != self.state and DEBUG:
            print(f"{saved_state} -> {self.state}", end="")


    def __init__(self):
        self.state = self.SSTV_IDLE
        self.radio = self._radio_create(RADIO_DEVICE)   # DRA818 Object
        self.radio.configRadio()
        self.modem = None       # Direwolf Modem Object
        self.subproc = None     # Spawn a subprocess
        self.direwolfproc = None # Spawn Direwolf subprocess
        self._timeout = None
        self._telemetry_timeout = None
        self._data_timeout = time()
        self._altitude = "undefined"
        self.data_source = self._telemetry()

        self._direwolf_killall()  

    # SUBPROCCESS METHODS
    # #####################################################
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
        self.subproc = subprocess.Popen(process_cmd) #,
#                stdout=subprocess.DEVNULL,
#                stderr=subprocess.DEVNULL)

    # RADIO METHODS
    # #####################################################
    def _radio_create(self, port_device: str):
        return DRA818(port_device)

    def _radio_enable(self, enable: bool):
        self.dbg_print(f"---------> _radio_enable {enable}")
        if self.radio is not None: 
            self.dbg_print(f"---------> _radio_enable new_state {enable}")
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
        return self.state not in (self.SSTV_IDLE, self.TELEMETRY_IDLE)

    # DIREWOLF_METHODS
    # #####################################################
    def _direwolf_killall(self):
        subprocess.Popen(["sudo", "killall", "-9", "direwolf"])

    def _direwolf_cleanup(self):
        if self.direwolfproc is not None:
            self.direwolfproc.kill()
            self.direwolfproc = None

    def _direwolf_poll(self):
        if self.direwolfproc is not None:
            self.direwolfproc.poll()
            return self.direwolf.returncode
        return -1

    def _direwolf_spawn(self):
        configfile_location = os.path.dirname(__file__) + "/" + "direwolf.conf.server"
        self.direwolfproc = subprocess.Popen(
                ["direwolf", "-c", configfile_location])
#                stdout=subprocess.DEVNULL,
#                stderr=subprocess.DEVNULL)

    # TELEMETRY SOURCE FUNCTIONS
    # #####################################################
    def _telemetry(self):
        return ser_io.serial_terminal(
                DATA_DEVICE,
                BAUD,
                timeout = 0.25)

    def _telemetry_forced_update(self):
        if self._data_timeout is None:
            self._telemetry_timer_update()
        if time() > self._data_timeout:
            self._data_timeout += self.TELEMETRY_TIMEOUT
            return True
        return False

    def _telemetry_timer_update(self):
        self._data_timeout = time() + self.TELEMETRY_TIMEOUT

    # MODEM CONTROL FUNCTIONS
    # #####################################################
    def _modem_connect(self):
        if self.modem is None:
            self.modem = direwolf_io.Direwolf(
                    "127.0.0.1", 
                    "8001", 
                    SSID_FROM, 
                    SSID_TO)

    def _modem_disconnect(self):
        del(self.modem)
        self.modem = None

    def _modem_write(self, line):
        self.dbg_print(f"Kom ik hier ({self.modem} | ({len(line)})" )
        if self.modem is not None and len(line):
            self.dbg_print("Pass to here?")
            self.modem.write(line)


    # RUNNER
    # #####################################################
    def run(self, restart: bool = False) -> bool:
        """
            Main runner. 

            @param restart: reset state machine and restart from the beginning
            @return done: true, false
        """
        saved_state = self.state


        # Common Code
        if self.data_source is not None:
            line = self.data_source.readline()
            if len(line):
                self.dbg_print(f"--> ({len(line)}){line}")
                telemetry_data = line
                self._data_timeout = time()
            else:
                telemetry_data = ""

        if self._telemetry_forced_update():
            telemetry_data = self.TELEMETRY_DUMMY
        
        if len(telemetry_data):
            self.dbg_print(f"data: {telemetry_data}")



        if restart:
            self.state = self.CAPTURE

        # SSTV STATEMACHINE 
        # #############################
        if self.state == self.CAPTURE:

            # Start CAPTURE
            self._subprocess_cleanup()
            self._subprocess_spawn(["./capture.sh", str(self.altitude)])
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
                self._subprocess_spawn(["./play.sh"])
                self.state = self.TRANSMITTING
                self._timeout = time() + self.TIMEOUT_TRANSMIT
            else:
                self.state = self.IDLE

        elif self.state == self.TRANSMITTING:
            if self._subprocess_poll() == 0:

                # Transmit complete
                self._radio_PTT(False)
                self._radio_enable(False)
                self.state = self.SSTV_IDLE
            elif time() > self._timeout:

                # Timout occurred
                self._radio_PTT(False)
                self._radio_enable(False)
                self._subprocess_cleanup()
                self.state = self.SSTV_IDLE

        elif self.state == self.SSTV_IDLE:
            self.state = self.TELEMETRY_CONNECTING

        # TELEMETRY STATEMACHINE
        # #############################
        elif self.state == self.TELEMETRY_SETUP:
            pass

        elif self.state == self.TELEMETRY_CONNECTING:
            # Make connection to Direwolf (TCP)
            self._direwolf_spawn()
            sleep(1)
            try: 
                self._modem_connect()
            except: 
                self._modem_disconnect()
            self.state = self.TELEMETRY_CONNECTED
            self._telemetry_timeout = time() + (TELEMETRY_DURATION * 60)
            self._data_timeout = time()

        elif self.state == self.TELEMETRY_CONNECTED:
            # Transmit to Direwolf via KISS
            if len(telemetry_data):
                # TODO Add to log
                self._modem_write(telemetry_data)

            if time() >= self._telemetry_timeout:
                self.state = self.TELEMETRY_BREAKDOWN

        elif self.state == self.TELEMETRY_BREAKDOWN:
            # Disconnect KISS TCP connection
            self._modem_disconnect()

            # Kill direwolf
            self._direwolf_cleanup()
            self.state = self.TELEMETRY_IDLE

        elif self.state == self.TELEMETRY_IDLE:
            self.state = self.CAPTURE

        elif self.state == self.RESTART:
            # If something really goes wrong
            self._subprocess_cleanup()
            self._direwolf_cleanup()
            pass

        else:
            self.state = self.IDLE

        self.dbg_state_change(saved_state)


if __name__ == "__main__":
    tele = Telemetry()
    
    i = 0

    while True: 
        i = i + 1
        tele.altitude = i * 10
        tele.run()

        if tele.is_busy():
            print("+", end="")
        else:
            print("-", end="")
        sys.stdout.flush()
        sleep(0.2)

    print("")
