import asyncio
from random import random
from communication import communication_protocol
from communication.communication_protocol import *

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
        ##registered users
        self.registeredUsers = {}
        self.userToContacts = {}
        self.command_protocol = Protocol()

    def uid_exists(self, uid):
        if uid in self.uidToConnectionUser:
            return True
        return False

    def add_connection(self, uid, connection):
        self.n_connections += 1
        self.uidToConnectionUser[uid] = {'user' : None, 'connection' : connection}
        print("New connection with uid '{}'".format(uid))
        print("Number of connections is '{}'".format(self.n_connections))

    def remove_connection(self, uid):
        self.n_connections -= 1
        user = self.uidToConnectionUser[uid]['user']
        print(user)
        del self.uidToConnectionUser[uid]
        if user:
            del self.userToUid[user]
        print("Connection from uid '{}' was removed".format(uid))
        print("Number of connections is '{}'".format(self.n_connections))

    def user_logged(self, uid, user):
        self.uidToConnectionUser[uid]['user'] =  user
        connection = self.uidToConnectionUser[uid]['connection']
        self.userToUid[user] = uid
        print("User '{}' logged to connection uid '{}'".format(user, uid))

    def user_dislogged(self, user):
        uid = self.userToUid[user]
        del self.userToUid[user]
        self.uidToConnectionUser[uid]['user'] =  None
        print("User '{}' dislogged from connection uid '{}'".format(user, uid))

    def process_data(self, uid, data):
        user = self.uidToConnectionUser[uid]['user']
        connection = self.uidToConnectionUser[uid]['connection']
        if user:
            print("Data received from a logged connection - username: {}".format(user))
            logged = True
        else:
            print("Data received from a dislogged connection")
            logged = False
        messageTuple = self.command_protocol.decode(data)
        print("RESULT OF PROCESS '{}'".format(messageTuple))
        response = self.exec_command(messageTuple, uid, user, logged)
        if response:
            print(response)
            response = self.command_protocol.encode(response)
            connection.send_client(response)

    def exec_command(self, messageTuple, uid, user, logged):
        result = messageTuple[0]
        if result == communication_protocol.OK:
            cmd = messageTuple[1]
            date = messageTuple[2]
            args = cmd.get_args()
            print("'{}' parameteres {}".format(cmd, args))
            if   isinstance(cmd, Login):
                username = args['username']
                passwd = args['passwd']
                if not username in self.userToUid:
                    if username in self.registeredUsers:
                        userpass = self.registeredUsers[username]
                        if passwd == userpass:
                            self.user_logged(uid, username)
                            result = 1
                        else:
                            result = 0
                    else:
                        result = -1
                else:
                    result = 2
                return LoginResult(result=result)
            elif isinstance(cmd, Register):
                username = args['username']
                passwd = args['passwd']
                if username in self.registeredUsers:
                    result = 0
                else:
                    self.registeredUsers[username] = passwd
                    result = 1
                return RegisterResult(result=result)
            else:
                if logged:
                    if isinstance(cmd, SendMessage):
                        to = args['to']
                        if to in self.userToUid:
                            responseUID = self.userToUid[to]
                            connectionToRespond = self.uidToConnectionUser[responseUID]['connection']
                            encodedCommand = self.command_protocol.encode(cmd)
                            connectionToRespond.send_client(encodedCommand)
                            result = 1
                        else:
                            result = 0
                        return SendMessageResult(result=result, to=to)
                    elif isinstance(cmd, AddContact):
                        contact = args['user']
                        if contact in self.registeredUsers:
                            if user in self.userToContacts[user]:
                                self.userToContacts[user].append(contact)
                            else:
                                self.userToContacts[user] = [contact]
                            result = 1
                        else:
                            result = 0
                        return AddContactResult(result=result)
                    elif isinstance(cmd, GetContacts):
                        if user in self.userToContacts:
                            result = self.userToContacts[user]
                        else:
                            result = []
                        return GetContactsResult(result=result)
                else:
                    print('Ignoring command {} cause connection is dislogged.'.format())
        else:
            print('Command is not valid. Code: {}'.format(result))
            return InvalidCommand(code=result)


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
            uid = MAX_UID * random()
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
        self.master.process_data(self.uid, data)

    def send_client(self, msg):
        print("Sending data to connection with uid '{}'".format(self.uid))
        self.transport.write(msg)