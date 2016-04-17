from tkinter import *
import asyncio
from functools import wraps
from communication import chatclient

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

class MyGui():
    
    def __init__(self):
        self.anchor = CENTER

        self.connection_try = None
        self.loop = asyncio.get_event_loop()
        self.client = chatclient.Client(self.loop, '127.0.0.1', 8888)
        self.messages = None
        
        self.root = self.init_root()
        self.loginScreen = self.build_login_frame()
        self.testScreen = self.build_login_new()

        self.raise_frame(self.loginScreen)

        self.log('Application started.')

    def init_root(self):
        root = Tk()
        root.title(APP_NAME)
        root.geometry('{}x{}'.format(WIDTHPIXELS, HEIGHTPIXELS))
        self.center(root)

        return root

    def build_login_frame(self):
        mainFrame = Frame(self.root, bd=1, relief=SUNKEN)

        loginFrame = Frame(mainFrame, bd=1, relief=SUNKEN)
        loginFrame.pack(anchor=self.anchor, fill=X)
        
        nameWindow = Frame(loginFrame)
        nameWindow.pack()
        userNameLabel = Label(nameWindow, text="User Name")
        userNameLabel.pack()
        userNameEntry = Entry(loginFrame)
        userNameEntry.pack()
        
        passwdWindow = Frame(loginFrame)
        passwdWindow.pack()
        userPasswdLabel = Label(passwdWindow, text="Password")
        userPasswdLabel.pack()
        userPasswdEntry = Entry(passwdWindow)
        userPasswdEntry.pack()

        buttonFrame = Frame(loginFrame, height=2, bd=1, relief=SUNKEN)
        buttonFrame.pack(fill=Y)
        login = Button(buttonFrame, text='Login', command= lambda: self.raise_frame(self.testScreen, self.loginScreen))
        login.pack()

        consoleFrame = Frame(mainFrame)
        consoleFrame.pack(fill=BOTH)
        scrollbar = Scrollbar(consoleFrame)
        scrollbar.pack(fill=Y, side=RIGHT)
        self.messages = Text(consoleFrame, background='white', bd=2, relief=SUNKEN, state=DISABLED, yscrollcommand=scrollbar.set)
        self.messages.pack(fill=BOTH)
        scrollbar.config(command=self.messages.yview)

        registrationFrame = Frame(mainFrame, bd=1, relief=SUNKEN)
        registrationFrame.pack(anchor=self.anchor, fill=BOTH, side=BOTTOM)
        teste = Button(registrationFrame, text='Register', command= lambda: self.log('to testando :D'))
        teste.pack(side=BOTTOM)

        return mainFrame

    def build_login_new(self):

        mainFrame = Frame(self.root, bd=1, relief=SUNKEN)

        loginFrame = Frame(mainFrame, bd=1, relief=SUNKEN)
        loginFrame.pack(anchor=self.anchor, fill=X)
        
        nameWindow = Frame(loginFrame)
        nameWindow.pack()
        userNameLabel = Label(nameWindow, text="User Name")
        userNameLabel.pack()
        userNameEntry = Entry(loginFrame)
        userNameEntry.pack()

        return mainFrame
        
    def raise_frame(self, frame, kill_frame=None):
        if kill_frame:
            self.kill_frame(kill_frame)
        frame.pack()

    def kill_frame(self, frame):
        frame.pack_forget()

    def log(self, message):
        self.messages.config(state=NORMAL)
        self.messages.insert(END, message + '\n')
        self.messages.config(state=DISABLED)

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

if __name__ == "__main__":
    gui = MyGui()
    gui.run()