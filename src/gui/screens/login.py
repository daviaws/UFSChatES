from tkinter import *

from observers.gui_events import event_login, event_register
from gui.widgets.text_box import TextBox

class LoginScreen():
    
    def __init__(self, master, root, anchor=CENTER):
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
        userPasswdEntry = Entry(passwdFrame, show="*")
        userPasswdEntry.pack()

        buttonFrame = Frame(loginFrame, height=2, bd=1, relief=SUNKEN)
        buttonFrame.pack(fill=Y)
        login = Button(buttonFrame, text='Login', command= lambda: self.master.update(event_login, username=userNameEntry.get(), passwd=userPasswdEntry.get()))
        login.pack()

        self.messages = TextBox(self.mainFrame)

        registrationFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        registrationFrame.pack(anchor=anchor, fill=BOTH, side=BOTTOM)
        register = Button(registrationFrame, text='Register', command= lambda: self.master.update(event_register, username=userNameEntry.get(), passwd=userPasswdEntry.get()))
        register.pack()

    def raises(self):
        self.mainFrame.pack(expand=True, fill=BOTH)

    def fall(self):
        self.mainFrame.pack_forget()

    def log(self, message):
        self.messages.log(message)
