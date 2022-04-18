###########################################################
# Serial Interface Helper                                 #
#                                                         #
###########################################################
import serial, io


def serial_terminal(device: str, baudrate: str, timeout: float):
    '''
        Creates a terminal interface using the given device.
        The terminal interface is line based.

        @param device: Full path to device (linux) (string)
        @param baudrate: Baudrate (as string)
        @param timeout: timeout in seconds (as float)
        
        Reading from serial terminal:
          use: readline() or readlines()

        Writing to serial terminal:
          use: write() or writelines()

        !! Be aware that this terminal buffers received data in
        FiFo order. readline reads the oldest first. readlines
        a list of all lines buffered.
    '''
    ser = serial.Serial(port=device, baudrate=baudrate, timeout=timeout)
    return io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def serial_interface(baudrate: str, device: str):
    return serial.Serial(device, baudrate)

if __name__ == "__main__":
    sio = serial_terminal('/dev/ttyUSB2', 9600, 0.25)

    import pdb; pdb.set_trace()

    while(True):
        line =  sio.readline()
        if len(line):
            print("Line: {}".format(line))