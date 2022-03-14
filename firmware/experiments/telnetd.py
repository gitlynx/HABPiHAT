# Telnet Daemon
################3
import asyncio, telnetlib3
import pdb


@asyncio.coroutine
def shell(reader, writer):
    writer.write('\r\nWould you like to play a game? ')
    line = ""
    while True:
        inp = yield from reader.read(1)
        if inp:
            if inp in '\b\x7f':
                inp = '\b \b'
                line = line[:-1]
            elif inp in '\r\n':
                # Parse line
                writer.write("\n\rThe input was: {}\n\r".format(line))
                line = ""
            elif inp in '\x03':
                writer.write("\n\rCtrl+C seen. Terminate connection\n\r")
                break
            else:
                line += inp
            writer.echo(inp)
            yield from writer.drain()
    writer.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(port=6023, shell=shell)
    server = loop.run_until_complete(coro)
    loop.run_until_complete(server.wait_closed())

