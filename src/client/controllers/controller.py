from datetime import datetime

from tkinter import *

import asyncio
from functools import wraps

from communication import chatclient
from communication.communication_protocol import Register, Login, SendMessage

from observers.observer import Observer
from observers.gui_events import *
from observers.model_events import *

from client.message_manager import MessageManager
from gui.controller.windows_manager import WindowsManager

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
        self.msg_man = MessageManager()

        self.mainWindow = main.MainWindow(app_name)
        root = self.mainWindow.get_root()
        self.addContactWindow = add_contact.AddContactWindow(self)

        self.loginScreen = login.LoginScreen(self, root)
        self.loginScreen.raises()
        self.loggedScreen = logged.LoggedScreen(self, root)

        self.loginScreen.log('Application started.')

    def update(self, *args, **kwargs):
        print("Event '%s' with args %s" % (args[0], kwargs))
        event = args[0]
        if event == event_internal_message:
            self.on_received_internal_message(**kwargs)
        
        elif event == event_pressed_send_login:
            self.on_pressed_send_login(**kwargs)
        
        elif event == event_pressed_send_register:
            self.on_pressed_send_register(**kwargs)
        
        elif event == event_login_result:
            self.login_result(**kwargs)
        
        elif event == event_register_result:
            self.register_result(**kwargs)
        
        elif event == event_popup_add_contact:
            self.popup_add_contact()
        
        elif event == event_pressed_add_contact:
            self.on_pressed_add_contact(**kwargs)
        
        elif event == event_open_chat_window:
            self.on_open_chat_window(**kwargs)
        
        elif event == event_closed_chat_window:
            self.on_close_chat_window(**kwargs)
        
        elif event == event_pressed_send_message:
            self.send_message(**kwargs)

        elif event == event_send_message_result:
            self.send_message_result(**kwargs)

    def on_received_internal_message(self, **kwargs):
        msg = kwargs['msg']
        self.loginScreen.log(msg)

    def on_pressed_send_login(self, **kwargs):
        username = kwargs['username']
        passwd = kwargs['passwd']
        self.client.send_command(Login(username=username, passwd=passwd))
        self.username = username

    def on_pressed_send_register(self, **kwargs):
        username = kwargs['username']
        passwd = kwargs['passwd']
        self.client.send_command(Register(username=username, passwd=passwd))

    def popup_add_contact(self, **kwargs):
        self.addContactWindow.raises()

    def on_pressed_add_contact(self, **kwargs):
        username = kwargs['username']
        print('Solicited to add user: "%s"' % username)

    def on_open_chat_window(self, **kwargs):
        username = kwargs['username']
        self.win_man.open(self, username)

    def on_close_chat_window(self, **kwargs):
        username = kwargs['username']
        self.win_man.close(username)      

    def send_message(self, **kwargs):
        fromuser = self.username
        to = kwargs['to']
        date = str(datetime.now())
        msg = kwargs['msg']
        if self.msg_man.has_pending_msg(to):
            chat_win = self.win_man.get_window(to)
            if chat_win:
                chat_win.pending_msg()
        else:
            self.msg_man.add_pending(to, msg)
            self.client.send_command(SendMessage(fromuser=fromuser, to=to, date=date, msg=msg))

    def send_message_result(self, **kwargs):
        result = kwargs['result']
        to = kwargs['to']
        if result == 1:
            #TODO - SAVE IN FILE ON SUCCESS
            msg = self.msg_man.get_msg(to)
            self.msg_man.remove_pending(to)
            chat_win = self.win_man.get_window(to)
            if chat_win:
                chat_win.msg_success()
        elif result == 0:
            self.msg_man.remove_pending(to)
            chat_win = self.win_man.get_window(to)
            if chat_win:
                chat_win.msg_fail()

    def login_result(self, **kwargs):
        result = kwargs['result']
        if result == 2:
            self.loginScreen.log('Login: User already logged')
        elif result == 1:
            self.loginScreen.fall()
            self.loggedScreen.raises()
            return
        elif result == 0:
            self.loginScreen.log('Login: Invalid password')
        elif result == -1:
            self.loginScreen.log('Login: Invalid user')
        self.username = None

    def register_result(self, **kwargs):
        result = kwargs['result']
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