import socket
import sys
import threading

from cmdr import Cmd, Cmdr
#from bmp388_sensor import BmpSensor

HOST = '0.0.0.0'
PORT = 1234

class SensorCmd(Cmd):

    def __init__(self, command: str) -> None:
        Cmd.__init__(self, command)
        #self.bmp = BmpSensor()

    def do_altitude(self, args):
        """ show altitude in [m] """
        print("Altitude: {:6.4f} m".format(self.bmp.get_altitude()))

    def do_temperature(self, args):
        """ show temperature in [°C] """
        print("Temperature: {:5.2f} °C".format(self.bmp.get_temperature()))

    def do_pressure(self, args):
        """ show pressure in [hPa] """
        print("Pressure: {:6.4f} hPa".format(self.bmp.get_pressure()))


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

    def do_help(self, args):
        """ show help """
        print("Built-in commands:")
        Cmd.do_help(self, args)

        print("Registered commands:")
        for module in self.commands.values():
            Cmd.do_help(module, args)
            #module.do_help(args)

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
        sensor_cmd = SensorCmd('sensor')
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
