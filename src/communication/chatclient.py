import asyncio
import time

class Client():

    def __init__(self, loop, ip, port):
        self.ip = ip
        self.port = port
        self.loop = loop
        self.connection = None
        self.connected = False

    @asyncio.coroutine
    def try_to_connect(self):
        while True:
            print("I'm trying")
            try:
                protocol = yield from asyncio.async(self.loop.create_connection(lambda: ClientConnection(self, self.loop), self.ip, self.port))
                self.connection = protocol[1]
            except ConnectionRefusedError as e:
                print("Can't connect: {}".format(e))
                print("Retrying in 5 seconds.")
                yield from asyncio.sleep(5)
            else:
                print("Connection is sucessfull")
                break

    def send_command(self, cmd):
        if self.connected:
            self.connection.send_server(cmd)
        else:
            print('Not connected to perform action')

class ClientConnection(asyncio.Protocol):

    master = None

    def __init__(self, master, loop):
        self.master = master
        self.loop = loop

    def send_server(self, msg):
        self.transport.write(msg.encode())

    def connection_made(self, transport):
        print('Connected!')
        self.transport = transport
        self.master.connected = True

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        self.master.connection = None
        self.master.connected = False
        asyncio.async(self.master.try_to_connect())
        print('The server closed the connection')
