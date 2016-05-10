from tkinter import *
import asyncio
from functools import wraps
from communication import chatclient
from communication.communication_protocol import Register, Login
from observers.observer import Observer

from observers.client_events import *


APP_NAME = 'UFSChat'
HEIGHTPIXELS = 600
WIDTHPIXELS = 300

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

class MyGui(Observer):
    
    def __init__(self):
        super().__init__()
        self.anchor = CENTER

        self.connection_try = None
        self.loop = asyncio.get_event_loop()
        self.client = chatclient.Client(self.loop, '127.0.0.1', 8888)
        
        self.root = self.init_root()
        self.loginScreen = LoginScreen(self, self.root, self.anchor)
        self.loginScreen.raises()
        self.loggedScreen = LoggedScreen(self, self.root, self.anchor)

        self.client.register(self)

        self.loginScreen.log('Application started.')

    def init_root(self):
        root = Tk()
        root.title(APP_NAME)
        root.geometry('%dx%d' % (WIDTHPIXELS, HEIGHTPIXELS))
        self.center(root)
        return root

    def update(self, *args, **kwargs):
        event = args[0]
        if event == event_internal_message:
            msg = kwargs['params']['msg']
            self.loginScreen.log(msg)
        elif event == event_login_result:
            result = kwargs['params']['result']
            if result == 2:
                self.loginScreen.log('Login: User already logged')
            elif result == 1:
                self.loginScreen.fall()
                self.loggedScreen.raises()
            elif result == 0:
                self.loginScreen.log('Login: Invalid password')
            elif result == -1:
                self.loginScreen.log('Login: Invalid user')
        elif event == event_register_result:
            result = kwargs['params']['result']
            if result == 1:
                self.loginScreen.log('Register: Sucess')
            elif result == 0:
                self.loginScreen.log('Register: User already exists')

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    @asyncio.coroutine
    def run_tk(self, root, interval=0.05):
        '''
        Run a tkinter app in an asyncio event loop.
        '''
        try:
            while True:
                self.root.update()
                yield from asyncio.sleep(interval)
        except TclError as e:
            if "application has been destroyed" not in e.args[0]:
                raise
            print('Application closed.')
            self.connection_try.cancel()

    @runloop
    def run(self):
        self.connection_try = asyncio.async(self.client.try_to_connect())
        yield from self.run_tk(self.root)

class LoginScreen():
    
    def __init__(self, master, root, anchor):
        self.master = master
        self.mainFrame = Frame(root, bd=1, relief=SUNKEN)

        loginFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        loginFrame.pack(anchor=anchor, fill=BOTH)
        
        nameFrame = Frame(loginFrame)
        nameFrame.pack()
        userNameLabel = Label(nameFrame, text="User Name")
        userNameLabel.pack()
        userNameEntry = Entry(nameFrame)
        userNameEntry.pack()
        
        passwdFrame = Frame(loginFrame)
        passwdFrame.pack()
        userPasswdLabel = Label(passwdFrame, text="Password")
        userPasswdLabel.pack()
        userPasswdEntry = Entry(passwdFrame)
        userPasswdEntry.pack()

        buttonFrame = Frame(loginFrame, height=2, bd=1, relief=SUNKEN)
        buttonFrame.pack(fill=Y)
        login = Button(buttonFrame, text='Login', command= lambda: self.master.client.send_command(Login(username=userNameEntry.get(), passwd=userPasswdEntry.get())))
        login.pack()

        self.messages = TextBox(self.mainFrame)

        registrationFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        registrationFrame.pack(anchor=anchor, fill=BOTH, side=BOTTOM)
        register = Button(registrationFrame, text='Register', command= lambda: self.master.client.send_command(Register(username=userNameEntry.get(), passwd=userPasswdEntry.get())))
        register.pack()

    def raises(self):
        self.mainFrame.pack(expand=True, fill=BOTH)

    def fall(self):
        self.mainFrame.pack_forget()

    def log(self, message):
        self.messages.log(message)

class LoggedScreen():

    def __init__(self, master, root, anchor):

        self.master = master
        self.mainFrame = Frame(root, bd=1, relief=SUNKEN)

        loggedFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        loggedFrame.pack(expand=True, fill=BOTH)

        login = Button(loggedFrame, text='Add contact', command= lambda: print('popup add contact'))
        login.pack()

        onlineFrame = Frame(loggedFrame, bd=1, relief=SUNKEN)
        onlineFrame.pack(expand=True, fill=BOTH)
        onlineFriendsLabel = Label(onlineFrame, text="Online Friends")
        onlineFriendsLabel.pack()
        self.onlineFriends = FriendList(master, onlineFrame)
        self.onlineFriends.able_chat()
        self.onlineFriends.reload(['one', 'two', 'three'])

        offlineFrame = Frame(loggedFrame, bd=1, relief=SUNKEN)
        offlineFrame.pack(expand=True, fill=BOTH)
        offlineFriendsLabel = Label(offlineFrame, text="Offline Friends")
        offlineFriendsLabel.pack()
        self.offlineFriends = FriendList(master, offlineFrame)
        self.offlineFriends.reload(['four', 'five', 'six'])

        logout = Button(loggedFrame, text='Logout', command= lambda: print('logout'))
        logout.pack()

    def raises(self):
        self.mainFrame.pack(expand=True, fill=BOTH)

    def fall(self):
        self.mainFrame.pack_forget()

class FriendList():

    def __init__(self, master, root):
        self.master = master

        self.listbox = Listbox(root, selectmode=SINGLE)
        self.listbox.pack(expand=True, fill=BOTH)

        self.menu = None
        self.chat = False

        self.listbox.bind('<Double-Button-1>', self.ondoubleclick)
        self.listbox.bind('<<ListboxSelect>>', self.onselect)
        self.listbox.bind('<3>', lambda e: self.context_menu(e))

    def able_chat(self):
        self.chat = True

    def reload(self, friend_list):
        self.listbox.delete(0, END)
        for item in friend_list:
            self.listbox.insert(END, item)

    def ondoubleclick(self, event):
        self.chat_contact(self.selection)

    def onselect(self, event):
        self.destroy_menu()
        w = event.widget
        index = int(w.curselection()[0])
        item = w.get(index)
        self.selection = item

    def context_menu(self, event):
        widget = event.widget
        index = widget.nearest(event.y)
        _, yoffset, _, height = widget.bbox(index)
        if event.y > height + yoffset + 5:
            self.destroy_menu()
            return
        item = widget.get(index)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(index)

        self.destroy_menu()
        self.menu = Menu(self.listbox, tearoff=0)
        self.menu.add_command(label="Add contact", command= lambda: print('popup add contact'))
        self.menu.add_separator()
        if self.chat:
            self.menu.add_command(label="Chat with '%s'" % (item), command= lambda: self.chat_contact(item))
        self.menu.add_command(label="Remove '%s'" % (item), command= lambda: self.remove_contact(item))
        self.menu.add_separator()
        self.menu.add_command(label="Exit menu", command=self.destroy_menu)
        self.menu.post(event.x_root, event.y_root)

    def chat_contact(self, contact):
        print ("Chat with '%s'" % (contact))

    def remove_contact(self, contact):
        print ("Remove '%s'" % (contact))

    def destroy_menu(self):
        if self.menu:
            self.menu.unpost()
            self.menu = None


class TextBox():

    def __init__(self, root):
        consoleFrame = Frame(root)
        consoleFrame.pack(expand=1, fill=BOTH)
        scrollbar = Scrollbar(consoleFrame)
        scrollbar.pack(fill=Y, side=RIGHT)
        self.messages = Text(consoleFrame, background='white', bd=2, relief=SUNKEN, state=DISABLED, yscrollcommand=scrollbar.set)
        self.messages.pack(expand=1, fill=BOTH)
        scrollbar.config(command=self.messages.yview)

    def log(self, message):
        self.messages.config(state=NORMAL)
        self.messages.insert(END, message + '\n')
        self.messages.config(state=DISABLED)
        self.messages.see(END)

    def able(self):
        self.messages.config(state=NORMAL)

    def disable(self):
        self.messages.config(state=DISABLED)

if __name__ == "__main__":
    gui = MyGui()
    gui.run()