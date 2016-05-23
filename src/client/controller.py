from datetime import datetime

from tkinter import *

import asyncio
from functools import wraps

from communication import chatclient
from communication.communication_protocol import *

from observers.observer import Observer

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

class Controller(Observer):

    def __init__(self, app_name, ip, port):
        self.username = None

        self.loop = asyncio.get_event_loop()

        self.connection_try = None
        self.client = chatclient.Client(self.loop, ip, port)
        self.client.register(self)

        self.get_contacts_call_later = None

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
        cmd = args[0]
        event = type(cmd)

        if event == InternalMessage:
            self.on_received_internal_message(cmd)
        
        elif event == Login:
            self.on_pressed_send_login(cmd)
        
        elif event == Register:
            self.on_pressed_send_register(cmd)
        
        elif event == LoginResult:
            self.login_result(cmd)
        
        elif event == RegisterResult:
            self.register_result(cmd)
        
        elif event == PopupAddContact:
            self.popup_add_contact(cmd)
        
        elif event == AddContact:
            self.on_pressed_add_contact(cmd)
        
        elif event == AddContactResult:
            self.add_contact_result(cmd)

        elif event == OpenChat:
            self.on_open_chat_window(cmd)
        
        elif event == CloseChat:
            self.on_close_chat_window(cmd)
        
        elif event == Message:
            arguments = cmd.get_args()
            to = arguments['to']
            if self.username == to:
                self.received_message(cmd)
            else:
                self.send_message(cmd)

        elif event == MessageResult:
            self.send_message_result(cmd)

        elif event == GetContactsResult:
            self.received_contacts_lists(cmd)

    def when_online(self):        
        self.get_contacts_routine()

    def get_contacts_routine(self):
        cmd = GetContacts()
        self.client.send_command(cmd)
        self.get_contacts_call_later = self.loop.call_later(5, self.get_contacts_routine)

    def on_received_internal_message(self, cmd):
        arguments = cmd.get_args()
        msg = arguments['msg']
        self.loginScreen.log(msg)

    def on_pressed_send_login(self, cmd):
        arguments = cmd.get_args()
        self.username = arguments['username']
        self.client.send_command(cmd)

    def on_pressed_send_register(self, cmd):
        self.client.send_command(cmd)

    def popup_add_contact(self, cmd):
        self.addContactWindow.raises()

    def on_pressed_add_contact(self, cmd):
        arguments = cmd.get_args()
        self.client.send_command(cmd)

    def on_open_chat_window(self, cmd):
        arguments = cmd.get_args()
        username = arguments['username']
        self.win_man.open(self, username)

    def on_close_chat_window(self, cmd):
        arguments = cmd.get_args()
        username = arguments['username']
        self.win_man.close(username)      

    def send_message(self, cmd):
        arguments = cmd.get_args()
        to = arguments['to']
        msg = arguments['msg']
        fromuser = self.username
        date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cmd.add_args(fromuser=fromuser, date=date)
        if self.msg_man.has_pending_msg(to):
            chat_win = self.win_man.get_window(to)
            if chat_win:
                chat_win.pending_msg()
        else:
            self.msg_man.add_pending(to, msg, date)
            self.client.send_command(cmd)

    def send_message_result(self, cmd):
        arguments = cmd.get_args()
        result = arguments['result']
        to = arguments['to']
        if result == 1:
            #TODO - SAVE IN FILE ON SUCCESS
            msg_result = self.msg_man.get_msg(to)
            msg = msg_result['msg']
            date = msg_result['date']
            self.msg_man.remove_pending(to)
            chat_win = self.win_man.get_window(to)
            if chat_win:
                chat_win.msg_success(self.username, date)
        elif result == 0:
            self.msg_man.remove_pending(to)
            chat_win = self.win_man.get_window(to)
            if chat_win:
                chat_win.msg_fail()

    def login_result(self, cmd):
        arguments = cmd.get_args()
        result = arguments['result']
        if result == 2:
            self.loginScreen.log('Login: User already logged')
        elif result == 1:
            self.loginScreen.fall()
            self.loggedScreen.raises()
            self.when_online()
            return
        elif result == 0:
            self.loginScreen.log('Login: Invalid password')
        elif result == -1:
            self.loginScreen.log('Login: Invalid user')
        self.username = None

    def register_result(self, cmd):
        arguments = cmd.get_args()
        result = arguments['result']
        if result == 1:
            self.loginScreen.log('Register: Success')
        elif result == 0:
            self.loginScreen.log('Register: User already exists')

    def received_message(self, cmd):
        arguments = cmd.get_args()
        fromuser = arguments['fromuser']
        to = arguments['to']
        date = arguments['date']
        msg = arguments['msg']
        #TODO - LOGAR EM ARQUIVO
        self.win_man.open(self, fromuser)
        chat_win = self.win_man.get_window(fromuser)
        chat_win.msg_received(date, msg)

    def received_contacts_lists(self, cmd):
        arguments = cmd.get_args()
        online_list = arguments['online']
        offline_list = arguments['offline']
        self.loggedScreen.reload_lists(online_list, offline_list)

    def add_contact_result(self, cmd):
        arguments = cmd.get_args()
        result = arguments['result']
        if result == 1:
            self.addContactWindow.clear()
        elif result == 0:
            self.addContactWindow.already_added()
        elif result == -1:
            self.addContactWindow.added_self()
        elif result == -2:
            self.addContactWindow.dont_exist()

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