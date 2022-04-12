import kiss
import aprs

class Direwolf():
    def __init__(self, host: str, port: str, source: str, destination:str):
        self.source = source
        self.destination = destination
        self.kiss_connection = kiss.TCPKISS(host=host, port=port)
        self.kiss_connection.start()

        pass

    def write(self, info: str):
        '''
            Create a new Frame and sent it
        '''
        if self.kiss_connection is not None:
            frame = aprs.Frame(self.source, self.destination, info=bytes(info, 'ascii'))
            encoded_frame = bytes(str(frame), 'ascii')          
            self.kiss_connection.write(encoded_frame)

    def _read_cb(self, frame):
        return self.read_cb(frame[1:].decode())

    def install_read_callback(self, read_cb):
        '''
            install callback function on KISS reception

            callback function prototype
            def read_cb(data: str)

            def print_frame(frame):
                print(aprs.Frame(frame[1:]))

        '''
        self.read_cb = read_cb
        self.kiss_connection.read(callback=self._read_cb)
