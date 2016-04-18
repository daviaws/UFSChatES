import asyncio
from random import random
from communication.communication_protocol import Protocol

class Server():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.server = None
        
        self.n_connections = 0
        #uid to connection/user dict
        self.uidToConnectionUser = {}
        ##user to connection/uid dict
        self.userToUid = {}
        
        self.command_protocol = Protocol()

    def uid_exists(self, uid):
        if uid in self.uidToConnectionUser:
            return True
        return False

    def add_connection(self, uid, connection):
        self.n_connections += 1
        self.uidToConnectionUser[uid] = {'user' : None, 'connection' : self}
        print("New connection with uid '{}'".format(uid))
        print("Number of connections is '{}'".format(self.n_connections))

    def remove_connection(self, uid):
        self.n_connections -= 1
        user = self.uidToConnectionUser[uid]['user']
        del self.uidToConnectionUser[uid]
        if user:
            del self.userToUid[user]
        print("Connection from uid '{}' was removed".format(uid))
        print("Number of connections is '{}'".format(self.n_connections))

    def user_logged(self, uid, user):
        self.uidToConnectionUser[uid]['user'] =  user
        connection = self.uidToConnectionUser[uid]['connection']
        self.userToUid[user] = {'uid' : uid, 'connection' : connection}
        print("User '{}' logged to connection uid '{}'".format(user, uid))

    def user_dislogged(self, user):
        uid = self.userToUid[user]
        del self.userToUid[user]
        self.uidToConnectionUser[uid]['user'] =  None
        print("User '{}' dislogged from connection uid '{}'".format(user, uid))

    def proccess_data(self, uid, data):
        user = self.uidToConnectionUser[uid]['user']
        if user:
            print("Data received from a logged connection - username: {}".format(user))
        else:
            print("Data received from a dislogged connection")
        result = self.command_protocol.decode(data)
        # MY WORK IS DONE FOR TODAY T_T
        print("RESULT OF PROCCESS '{}'".format(result))
        if result[0] == 0:
            print("'{}' parameteres {}".format(result[1], result[1].get_args()))

    def run(self):
        coroutine = self.loop.create_server(lambda: ServerConnection(self), self.ip, self.port)
        self.server = self.loop.run_until_complete(coroutine)

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        # Close the server
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

class ServerConnection(asyncio.Protocol):
    
    MAX_UID = 5000

    def __init__(self, master):
        self.master = master
        self.uid = self.generate_uid()

    def generate_uid(self):
        uid = str(int(self.MAX_UID * random()))
        while self.master.uid_exists(uid):
            uid = MAX_UID * random.random()
        return uid

    def connection_made(self, transport):
        self.master.add_connection(self.uid, self)
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self, exc):
        print("Lost connection from uid '{}'".format(self.uid))
        self.master.remove_connection(self.uid)

    def data_received(self, data):
        print("Received data from connection with uid '{}'".format(self.uid))
        self.master.proccess_data(self.uid, data)
