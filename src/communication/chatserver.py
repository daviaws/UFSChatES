import asyncio
from random import random
from communication import communication_protocol
from communication.communication_protocol import *
from communication import User
from communication import Rooms

from observers.observable import Observable

class Server(Observable):

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

        self.rooms = []
        self.users = []

    def uid_exists(self, uid):
        if uid in self.uidToConnectionUser:
            return True
        return False

    def user_by_uid(self, uid):
        return self.uidToConnectionUser[uid]['user']

    def connection_by_uid(self, uid):
        return self.uidToConnectionUser[uid]['connection']

    def add_connection(self, uid, connection):
        self.n_connections += 1
        self.uidToConnectionUser[uid] = {'user' : None, 'connection' : connection}
        print("New connection with uid '{}'".format(uid))
        print("Number of connections is '{}'".format(self.n_connections))

    def remove_connection(self, uid):
        self.n_connections -= 1
        user = self.user_by_uid(uid)
        del self.uidToConnectionUser[uid]
        if user:
            del self.userToUid[user]
        print("Connection from uid '{}' was removed".format(uid))
        print("Number of connections is '{}'".format(self.n_connections))

    def login_user(self, uid, username, password):
        if not username in self.userToUid:
            if username in self.registeredUsers:
                userpass = self.registeredUsers[username]
                if password == userpass:
                    self.user_logged(uid, username)
                    result = 1
                else:
                    result = 0
            else:
                result = -1
        else:
            result = 2
        return LoginResult(result=result)

    def user_logged(self, uid, user):
        self.uidToConnectionUser[uid]['user'] =  user
        connection = self.connection_by_uid(uid)
        self.userToUid[user] = uid
        print("User '{}' logged to connection uid '{}'".format(user, uid))

    def user_dislogged(self, user):
        uid = self.userToUid[user]
        del self.userToUid[user]
        self.uidToConnectionUser[uid]['user'] =  None
        print("User '{}' dislogged from connection uid '{}'".format(user, uid))

    def register_user(self, username, password):
        if username in self.registeredUsers:
            result = 0
        else:
            self.registeredUsers[username] = password
            self.userToContacts[username] = []
            result = 1
        return RegisterResult(result=result)

    def send_message(self, cmd):
        args = cmd.get_args()
        destiny = args['to']
        message = self.command_protocol.encode(cmd)
        result = 1

        if destiny in self.users:
            user = users[destiny]
            user.receive_message(message)
        elif destiny in self.rooms:
            room = rooms[destiny]
            room.broadcast_message(message)
        else:
            result = 0

        return MessageResult(result=result, to=toUser)
        
    def add_contact(self, user, contact):
        result = -2
        if contact in self.registeredUsers:
            result = -1
            if contact != user:
                result = 0
                if not contact in self.userToContacts[user]:
                    self.userToContacts[user].append(contact)
                    result = 1
        return AddContactResult(result=result)

    def get_contacts(self, user):
        contacts = self.userToContacts[user]
        online_list = []
        offline_list = []
        for item in contacts:
            if item in self.userToUid:
                online_list.append(item)
            else:
                offline_list.append(item)
        return GetContactsResult(online=sorted(online_list), offline=sorted(offline_list))        

    def create_rooms(self, admin_name, room_name):
        if room_name in self.rooms:
            result = 0
        else:
            room = Room(admin_name, room_name)
            rooms[room_name] = room
            result = 1
        return CreateRoomResult(result=result)        

    def process_data(self, uid, data):
        user = self.user_by_uid(uid)
        connection = self.connection_by_uid(uid)
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
        if result != communication_protocol.OK:
            print('Command is not valid. Code: {}'.format(result))
            return InvalidCommand(code=result)

        cmd = messageTuple[1]
        date = messageTuple[2]
        cmd_type = type(cmd)
        args = cmd.get_args()
        print("'{}' parameteres {}".format(cmd, args))

        if cmd_type == Login:
            username = args['username']
            password = args['passwd']
            return self.login_user(uid, username, password)
        
        if cmd_type == Register:
            username = args['username']
            password = args['passwd']
            return self.register_user(username, password)
        
        if logged:
            if cmd_type == Message:
                return self.send_message(cmd)
            elif cmd_type == AddContact:
                contact = args['username']
                return self.add_contact(user, contact)
            elif cmd_type == GetContacts:
                return self.get_contacts(user)
            elif cmd_type == CreateRoom:
                admin_name = user
                room_name = args['roomname']
                return self.create_room(admin_name, room_name)
        else:
            print('Ignoring command {} cause connection is dislogged.'.format(cmd))

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
            uid = self.MAX_UID * random()
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