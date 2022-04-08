import helpers.serial_interface as ser_io
import helpers.direwolf_interface as direwolf_io
import argparse
from operator import xor
from time import sleep


DEVICE = '/dev/ttySC0'
BAUD = '115200'



def server(baudrate: int=None , device: str=None, host: str = None, port: str=None):
    '''
        Message generator
        Retrieves information from external serial connected device
        and feeds it to Direwolf via (APRS/)KISS
    ''' 
    modem = direwolf_io.Direwolf(host, port, 'ON3JCO-11', 'ON4NOK')

    data_source = ser_io.serial_terminal(device, baudrate, timeout=0.25)

    while True:
        line = data_source.readline()
        if len(line):
            print("Line: {}".format(line))
            modem.write(line)


def printer(line: str):
    print(f"Line: {line}")

def client(host: str = None, port: str=None):
    '''
        Message consumer
        Receives from Direwolf via KISS
    '''
    modem = direwolf_io.Direwolf(host, port, 'ON4NOK', "ON3JCO-11")

    import pdb
    pdb.set_trace()

    modem.install_read_callback(printer)

    print("DO I start the loop?")

    while True:
        sleep(1) 
    pass


def argumentparsing():
    '''
        Parse commandline arguments and return an argument namespace
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="Starts program as data server", required=False, action="store_true", dest="server")
    parser.add_argument("--client", help="Starts program as data client", required=False, action="store_true", dest="client")
    parser.add_argument("host", help="Direwolf host name (or IP)", type=str)
    parser.add_argument("port", help="Direworl IP port", type=str)
    return parser.parse_args()

if __name__ == "__main__":
    
    arg_namespace = argumentparsing()

    if not xor(arg_namespace.server, arg_namespace.client): 
        print("Server/Client settings not compatible. check again")
        exit(1)

    if arg_namespace.server:
        print("Server")
        server(BAUD, DEVICE, arg_namespace.host, arg_namespace.port)
    elif arg_namespace.client:
        print("Client")
        client(arg_namespace.host, arg_namespace.port)
    else:
        print("Server nor client setting selected")
        pass        
