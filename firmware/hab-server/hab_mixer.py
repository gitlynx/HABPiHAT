'''
Alsa Mixer module
'''
import alsaaudio
import time

from threading import Thread
from cmdr import Cmd
from hab_logger import BaseLogger

class Mixer(Thread):
    ''' Alsa mixer class '''

    def __init__(self, logger: BaseLogger):
        Thread.__init__(self, name='Mixer')
        self._log = logger
        self._mixer: alsaaudio.Mixer = alsaaudio.Mixer('Headphone')
        self._mixer.setvolume(100)

    def run(self) -> None:
        self._log.log_info("Alsa mixer started")
        while True:
            self._mixer.setmute(False)
            self._log.log_info("Alsa mixer unmuted")
            time.sleep(10)
            self._mixer.setmute(True)
            self._log.log_info("Alsa mixer muted")
            time.sleep(50)

    def get_volume(self):
        return self._mixer.getvolume()

    def set_volume(self, value):
        self._mixer.setvolume(value)

    def mute(self):
        self._mixer.setmute(True)

    def unmute(self):
        self._mixer.setmute(False)

    def mute(self):
        self._mixer.setmute(True)

    def is_muted(self):
        return False if self._mixer.getmute()[0] == 0 else True

class MixerCmd(Cmd):
    '''
    Access Alsa Mixer from the command shell
    '''

    def __init__(self, mixer: Mixer) -> None:
        Cmd.__init__(self, 'mixer')
        self._mixer = mixer

    def do_volume(self, args=None):
        """ get/set volume """
        if args is not None:
            self._mixer.set_volume(int(args))
        print(f"Volume: {self._mixer.get_volume()}")

    def do_mute(self, args=None):
        """ get/set mute """
        if args is not None:
            if args == "on":
                self._mixer.mute()
            elif args == "off":
                self._mixer.unmute()
            else:
                pass
        if self._mixer.is_muted():
            print("Audio is muted")
        else:
            print("Audio is not muted")