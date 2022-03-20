import kiss
import aprs


HOST="192.168.1.62"
PORT="8001"


def p(x): print(x)  # prints whatever is passed in.




def main():
    frame = aprs.Frame()

    # import pdb; pdb.set_trace()

    frame = aprs.Frame(source='W2GMD-14', destination='PYKISS', info=bytes('>Hello World!', 'ascii'))
    ki = kiss.TCPKISS(host=HOST, port=PORT)
    ki.start()

    import pdb; pdb.set_trace()

    #ki.write(bytes(str(frame),'ascii'))
    encoded_frame = bytes(str(frame), 'ascii')
    ki.write(encoded_frame)

if __name__ == '__main__':
    main()