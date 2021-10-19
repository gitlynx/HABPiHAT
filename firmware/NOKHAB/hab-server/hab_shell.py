import socket
import sys

from cmdr import Cmdr
from threading import Thread

class HabShell(Cmdr, Thread):
    prompt = 'hab> '

    def __init__(self, sock:socket.socket):
        self._sock = sock
        sock_file = sock.makefile('rw')
        Cmdr.__init__(self, stdin=sock_file, stdout=sock_file)
        sys.stdout = sock_file
        Thread.__init__(self, name='HabPrompt', daemon=True)

    def do_exit(self, args):
        """ exit HAB shell """
        self.postloop()
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()

    def preloop(self):
        print('''
                    ,~-.
                   (  ' )-.          ,~'`-.
                ,~' `  ' ) )       _(   _) )
               ( ( .--.===.--.    (  `    ' )
                `.%%.;::|888.#`.   `-'`~~=~'
                /%%/::::|8888\##\\
               |%%/:::::|88888\##|
               |%%|:::::|88888|##|.,-.
               \%%|:::::|88888|##/    )_
                \%\:::::|88888/#/ ( `'  )
                 \%\::::|8888/#/(  ,  -'`-.
             ,~-. `%\:::|888/#'(  (     ') )
             (  ) )_ `\__|__/'   `~-~=--~~='
            ( ` ')  ) [VVVVV]
           (_(_.~~~'   \|_|/
                       [XXX]
                       `"""' 
        ''')
        print("Welcome to the HAB shell")

    def postloop(self):
        print("Thank you for flying HAB airlines", flush=True)

    def run(self) -> None:
        try:
            self.cmdloop()
        except:
            pass
        finally:
            self._sock.close()