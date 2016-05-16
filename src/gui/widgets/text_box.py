from tkinter import *

class TextBox():

    def __init__(self, root, able=DISABLED):
        consoleFrame = Frame(root)
        consoleFrame.pack(expand=1, fill=BOTH)
        scrollbar = Scrollbar(consoleFrame)
        scrollbar.pack(fill=Y, side=RIGHT)
        self.messages = Text(consoleFrame, background='white', bd=2, relief=SUNKEN, state=able, yscrollcommand=scrollbar.set)
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
