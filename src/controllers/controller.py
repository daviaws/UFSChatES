from tkinter import *
import asyncio
from functools import wraps

from communication import chatclient
from communication.communication_protocol import Register, Login

from observers.observer import Observer
from observers.gui_events import *
from observers.model_events import *

from gui.controllers.windows_manager import WindowsManager

from gui.windows import *
from gui.screens import *

def runloop(func):
    '''
    This decorator converts a coroutine into a function which, when called,
    runs the underlying coroutine to completion in the asyncio event loop.
    '''
    func = asyncio.coroutine(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = args[0].loop
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper

class Controller():

    def __init__(self, app_name, ip, port):
        self.loop = asyncio.get_event_loop()

        self.connection_try = None
        self.client = chatclient.Client(self.loop, ip, port)
        self.client.register(self)

        self.win_man = WindowsManager()

        self.mainWindow = main.MainWindow(app_name)
        root = self.mainWindow.get_root()
        self.addContactWindow = add_contact.AddContactWindow(self)
        self.chatWindows = []

        self.loginScreen = login.LoginScreen(self, root)
        self.loginScreen.raises()
        self.loggedScreen = logged.LoggedScreen(self, root)

        self.loginScreen.log('Application started.')

    def update(self, *args, **kwargs):
        print('Event %s with args %s' % (args, kwargs))
        event = args[0]
        if event == event_internal_message:
            msg = kwargs['msg']
            self.loginScreen.log(msg)
        elif event == event_login:
            username = kwargs['username']
            passwd = kwargs['passwd']
            self.client.send_command(Login(username=username, passwd=passwd))
        elif event == event_register:
            username = kwargs['username']
            passwd = kwargs['passwd']
            self.client.send_command(Register(username=username, passwd=passwd))
        elif event == event_login_result:
            result = kwargs['result']
            self.login_result(result)
        elif event == event_register_result:
            result = kwargs['result']
            self.register_result(result)
        elif event == event_popup_add_contact:
            self.addContactWindow.raises()
        elif event == event_pressed_add_contact:
            username = kwargs['username']
            print('Solicited to add user: "%s"' % username)
        elif event == event_open_chat_window:
            username = kwargs['username']
    
    def login_result(self, result):
        if result == 2:
            self.loginScreen.log('Login: User already logged')
        elif result == 1:
            self.loginScreen.fall()
            self.loggedScreen.raises()
        elif result == 0:
            self.loginScreen.log('Login: Invalid password')
        elif result == -1:
            self.loginScreen.log('Login: Invalid user')

    def register_result(self, result):
        if result == 1:
            self.loginScreen.log('Register: Success')
        elif result == 0:
            self.loginScreen.log('Register: User already exists')

    @asyncio.coroutine
    def run_tk(self, root, interval=0.05):
        '''
        Run a tkinter app in an asyncio event loop.
        '''
        try:
            while True:
                root.update()
                yield from asyncio.sleep(interval)
        except TclError as e:
            if "application has been destroyed" not in e.args[0]:
                raise
            print('Application closed.')
            self.connection_try.cancel()

    @runloop
    def run(self):
        self.connection_try = asyncio.async(self.client.try_to_connect())
        yield from self.run_tk(self.mainWindow.get_root())