import asyncio
import time
from communication.communication_protocol import Protocol

class Client():

    def __init__(self, loop, ip, port):
        self.ip = ip
        self.port = port
        self.loop = loop
        self.connection = None
        self.isconnected = False
        self.command_protocol = Protocol()

    @asyncio.coroutine
    def try_to_connect(self):
        while True:
            print("I'm trying")
            try:
                connection = yield from asyncio.async(self.loop.create_connection(lambda: ClientConnection(self, self.loop), self.ip, self.port))
                self.connection = connection[1]
            except ConnectionRefusedError as e:
                print("Can't connect: {}".format(e))
                print("Retrying in 5 seconds.")
                yield from asyncio.sleep(5)
            else:
                print("Connection is sucessfull")
                break

    def send_command(self, cmd):
        if self.isconnected:
            encodedCommand = self.command_protocol.encode(cmd)
            self.connection.send_server(encodedCommand)
        else:
            print('Not connected to perform action')

    def connected(self):
        self.isconnected = True

    def disconnected(self):
        self.connection = None
        self.isconnected = False

class ClientConnection(asyncio.Protocol):

    def __init__(self, master, loop):
        self.master = master
        self.loop = loop

    def send_server(self, msg):
        self.transport.write(msg)

    def connection_made(self, transport):
        print('Connected!')
        self.transport = transport
        self.master.connected()

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        self.master.disconnected()
        asyncio.async(self.master.try_to_connect())
        print('The server closed the connection')
