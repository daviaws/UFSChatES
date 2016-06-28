import base64
import json
from datetime import datetime
from copy import deepcopy

OK = 0
DATETIME_NONE = 1
CMD_NONE = 2
CMD_INVALID = 3
CMD_ARGS_INVALID = 4
ERROR_DECODING = 5

class Command():
    def __init__(self, *args, **kwargs):
        self.args = {}
        if kwargs:
            for key in kwargs:
                self.args[key] = kwargs[key]
        self.date = None
        self.keyargs = set()

    def add_args(self, **kwargs):
        if kwargs:
            for key in kwargs:
                self.args[key] = kwargs[key]

    def has_args(self):
        if self.args:
            return True
        return False

    def get_args(self):
        return deepcopy(self.args)

    def validate(self): 
        if self.keyargs:
            if not set(self.args) == self.keyargs:
                return False
        return True

    def __repr__(self):
        return "Type Command > '{}'".format(type(self).__name__)

#Chat
class Register(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'username', 'passwd'}

class RegisterResult(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'result'}
        
class Login(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'username', 'passwd'}

class LoginResult(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'result'}

class Message(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'to', 'fromuser', 'date', 'msg'}

class MessageResult(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'result', 'to'}

class GetContacts(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GetContactsResult(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AddContact(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
        self.keyargs = {'username'}

class AddContactResult(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'result'}

class CreateRoom(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'roomname'}

class CreateRoomResult(Command)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'result'}

#GUI BIND EVENTS
class InternalMessage(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'msg'}

class PopupAddContact(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class OpenChat(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CloseChat(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#INVALID
class InvalidCommand(Command):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyargs = {'code'}

class Protocol():

    REF_DICT = {
    'Login' : Login, 'LoginResult' : LoginResult, 'Register' : Register,
    'RegisterResult' : RegisterResult, 'Message' : Message, 'MessageResult' : MessageResult,
    'PopupAddContact' : PopupAddContact, 'AddContact' : AddContact, 'AddContactResult' : AddContactResult,
    'InvalidCommand' : InvalidCommand, 'InternalMessage' : InternalMessage, 'GetContacts' : GetContacts,
    'GetContactsResult' : GetContactsResult, 'CreateRoom' : CreateRoom, 'CreateRoomResult' : CreateRoomResult
    }

    def encode(self, cmd):
        cmd_name = type(cmd).__name__
        date = str(datetime.now())
        if cmd.has_args():
            encodedCommand = {'cmd' : cmd_name, 'datetime' : date, 'params' : cmd.get_args()}
        else:
            encodedCommand = {'cmd' : cmd_name, 'datetime' : date}
        encodedCommand = json.dumps(encodedCommand)
        encodedCommand = encodedCommand.encode('ascii')
        encodedCommand = base64.b64encode(encodedCommand)
        return encodedCommand

    def decode(self, data):
        try:
            decodedCommand = base64.b64decode(data)
            decodedCommand = decodedCommand.decode('ascii')
            decodedCommand = json.loads(decodedCommand)
            if 'datetime' not in decodedCommand:
                print('OPSSS, I dont have a date... D:')
                return (DATETIME_NONE,)

            if 'cmd' not in decodedCommand:
                print('OPSSS, I dont have a command... D:')
                return (CMD_NONE,)

            datetime = decodedCommand['datetime']
            cmd = self.REF_DICT[decodedCommand['cmd']]
            if decodedCommand['cmd'] in self.REF_DICT:
                if 'params' in decodedCommand:
                    cmd = cmd(**decodedCommand['params'])
                else:
                    cmd = cmd()

                if cmd.validate():
                    return (OK, cmd, datetime)
                else:
                    print("Command is incompatible with '{}'".format(cmd))
                    return (CMD_ARGS_INVALID,)
            else:
                print('OPSSS, invalid command D:')
                return (CMD_INVALID,)
        except Exception as e:
            print('Exception caught in decoding data: {}'.format(e))
            return (ERROR_DECODING,)
            