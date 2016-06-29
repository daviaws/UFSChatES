import asyncio
from random import random
from communication import communication_protocol
from communication.communication_protocol import *
from communication.user import User
from communication.room import Room

from observers.observable import Observable

class Server(Observable):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.server = None
        
        self.rooms = {}
        self.users = {}
        
        self.n_connections = 0
        self.uidToUser = {}
        
        self.command_protocol = Protocol()

    def uid_exists(self, uid):
        if uid in self.uidToUser:
            return True
        return False

    def user_by_uid(self, uid):
        if uid in self.uidToUser:
            return self.uidToUser[uid]
        return None

    def add_connection(self):
        self.n_connections += 1
        print("Number of connections is '{}'".format(self.n_connections))

    def remove_connection(self, uid):
        user = self.user_by_uid(uid)
        if user:
            self.user_dislogged(user)
        self.n_connections -= 1
        print("Number of connections is '{}'".format(self.n_connections))

    def login_user(self, uid, connection, username, password):
        if username in self.users:
            user = self.users[username]
            if not user.logged():
                if user.password_matchs(password):
                    self.user_logged(uid, connection, user)
                    result = 1
                else:
                    result = 0
            else:
                result = 2
        else:
            result = -1
        return LoginResult(result=result)

    def user_logged(self, uid, connection, user):
        self.uidToUser[uid] =  user
        user.login(uid, connection)
        print("User '{}' logged to connection uid '{}'".format(user.name, uid))

    def user_dislogged(self, user):
        uid = user.uid
        user.logout()
        del self.uidToUser[uid]
        print("User '{}' dislogged from connection uid '{}'".format(user.name, uid))

    def register_user(self, username, password):
        if username in self.users:
            result = 0
        else:
            self.users[username] = User(username, password)
            result = 1
        return RegisterResult(result=result)

    def send_message(self, cmd):
        args = cmd.get_args()
        destiny = args['to']
        message = self.command_protocol.encode(cmd)
        result = 1

        if destiny in self.users:
            user = self.users[destiny]
            user.receive_message(message)
        elif destiny in self.rooms:
             room = self.rooms[destiny]
             room.broadcast_message(message)
        else:
            result = 0

        return MessageResult(result=result, to=destiny)
        
    def add_contact(self, user, contact):
        result = -2
        if contact in self.users:
            result = -1
            if contact != user.name:
                result = 0
                if not contact in user.get_contacts():
                    user.add_contact(contact)
                    result = 1
        return AddContactResult(result=result)

    def remove_contact(self, user, contact):
        result = 0
        if contact in user.get_contacts():
            user.remove_contact(contact)
            result = 1

        return RemoveContactResult(result=result)

    def get_contacts(self, user):
        contacts = user.get_contacts()
        online_list = []
        offline_list = []
        for item in contacts:
            if item in self.users:
                if self.users[item].logged():
                    online_list.append(item)
                else:
                    offline_list.append(item)
            else:
                raise Exception('Not Implemented #User dont exist anymore#')
        return GetContactsResult(online=sorted(online_list), offline=sorted(offline_list))        

    def create_room(self, admin_name, room_name):
        if room_name in self.rooms:
            result = 0
        else:
            room = Room(admin_name, room_name)
            self.rooms[room_name] = room
            result = 1
        return CreateRoomResult(result=result)        

    def join_room(self, user, room_name):
        if room_name in self.rooms:
            user.join_room(room_name)
            room = self.rooms[room_name]
            room.add_user(user)
            result = 1
        else:
            result = 0
        
        return JoinRoomResult(result=result)

    def leave_room(self, user, room_name):
        if room_name in user.get_rooms():
            room = self.rooms[room_name]
            room.remove_user(user)
            user.exit_room(room_name)
            result = 1
        else:
            result = 0

        return LeaveRoomResult(result=result)

    def process_data(self, uid, connection, data):
        user = self.user_by_uid(uid)
        if user:
            print("Data received from a logged connection - username: {}".format(user))
            logged = True
        else:
            print("Data received from a dislogged connection")
            logged = False
        messageTuple = self.command_protocol.decode(data)
        print("RESULT OF PROCESS '{}'".format(messageTuple))
        response = self.exec_command(messageTuple, uid, connection, user, logged)
        if response:
            print(response)
            response = self.command_protocol.encode(response)
            connection.send_client(response)

    def exec_command(self, messageTuple, uid, connection, user, logged): 
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
            return self.login_user(uid, connection, username, password)
        
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
            elif cmd_type == RemoveContact:
                contact = args['username']
                return self.remove_contact(user, contact)
            elif cmd_type == GetContacts:
                return self.get_contacts(user)
            elif cmd_type == CreateRoom:
                admin_name = user.name
                room_name = args['roomname']
                return self.create_room(admin_name, room_name)
            elif cmd_type == JoinRoom:
                room_name = args['roomname']
                return self.join_room(user, room_name)
            elif cmd_type == LeaveRoom:
                room_name = args['roomname']
                return self.leave_room(user, room_name)

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
        self.master.add_connection()
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self, exc):
        print("Lost connection from uid '{}'".format(self.uid))
        self.master.remove_connection(self.uid)

    def data_received(self, data):
        print("Received data from connection with uid '{}'".format(self.uid))
        self.master.process_data(self.uid, self, data)

    def send_client(self, msg):
        print("Sending data to connection with uid '{}'".format(self.uid))
        self.transport.write(msg)
