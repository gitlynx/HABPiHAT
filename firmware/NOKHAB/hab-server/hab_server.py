import socket
import sys
import threading

from cmdr import Cmdr
from sensor import Sensor, SensorCmd

HOST = '0.0.0.0'
PORT = 1234

sensor: Sensor = Sensor()
sensor_cmd: SensorCmd = SensorCmd(sensor)

class HabPrompt(Cmdr):
    prompt = 'hab> '

    def __init__(self, sock:socket.socket):
        self._sock = sock
        sock_file = sock.makefile('rw')
        Cmdr.__init__(self, stdin=sock_file, stdout=sock_file)
        sys.stdout = sock_file
        self.use_rawinput = False

    def do_exit(self, args):
        """ exit HAB shell """
        print("Thank you for flying HAB airlines", flush=True)
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
        print("Thank you for flying HAB airlines")

def service_connection(sock:socket.socket, address):
    try:
        print(address)
        p = HabPrompt(sock)
        p.register(sensor_cmd)
        p.cmdloop()
    except:
        pass
    finally:
        sock.close()
        return False

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        try:
            client, address = s.accept()
            client.settimeout(None)
            thread = threading.Thread(target=service_connection, args=(client, address))
            thread.daemon = True
            thread.start()
        except KeyboardInterrupt:
            print('Exiting')
            sys.exit(0)
