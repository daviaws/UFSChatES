import asyncio
import time
from communication.communication_protocol import *
from observers.observable import Observable

class Client(Observable):

    def __init__(self, loop, ip, port):
        super().__init__()
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
                self.internal_msg("Can't connect: {}".format(e))
                self.internal_msg("Retrying in 5 seconds.")
                yield from asyncio.sleep(5)
            else:
                self.internal_msg("Connection is sucessfull")
                break

    def send_command(self, cmd):
        print('Send command "%s" to server' % cmd)
        if self.isconnected:
            encodedCommand = self.command_protocol.encode(cmd)
            self.connection.send_server(encodedCommand)
        else:
            self.internal_msg('Not connected to perform action')

    def connected(self):
        self.isconnected = True

    def disconnected(self):
        self.internal_msg('Connection with Server is down.')
        self.connection = None
        self.isconnected = False

    def proccess_data(self, data):
        messageTuple = self.command_protocol.decode(data)
        print("RESULT OF PROCCESS '{}'".format(messageTuple))
        result = messageTuple[0]
        if result == OK:
            cmd = messageTuple[1]
            date = messageTuple[2]
            args = cmd.get_args()
            print("'{}' parameteres {}".format(cmd, args))
            self.update_observers(cmd)
        else:
            self.internal_msg('Command is not valid. Code: {}'.format(result))
            return InvalidCommand(code=result)

    def internal_msg(self, msg):
        cmd = InternalMessage(msg=msg)
        self.update_observers(cmd)

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
        print('Data received from Server')
        self.master.proccess_data(data)

    def connection_lost(self, exc):
        self.master.disconnected()
        asyncio.async(self.master.try_to_connect())
