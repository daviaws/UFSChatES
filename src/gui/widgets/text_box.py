from tkinter import *

class TextBox():

    def __init__(self, root, able=DISABLED):
        if able == DISABLED:
            self.able = False
        elif able == Normal:
            self.able = True
        consoleFrame = Frame(root)
        consoleFrame.pack(expand=1, fill=BOTH)
        scrollbar = Scrollbar(consoleFrame)
        scrollbar.pack(fill=Y, side=RIGHT)
        self.messages = Text(consoleFrame, background='white', bd=2, relief=SUNKEN, state=able, yscrollcommand=scrollbar.set)
        self.messages.pack(expand=1, fill=BOTH)
        scrollbar.config(command=self.messages.yview)

    def log(self, message):
        if self.able:
            self.messages.insert(END, message + '\n')
            self.messages.insert(END, message + '\n')
        else:
            self.messages.config(state=NORMAL)
            self.messages.insert(END, message + '\n')
            self.messages.config(state=DISABLED)
            self.messages.see(END)

    def get_text(self):
        return self.messages.get("1.0",END)

    def clean(self):
        if self.able:
            self.messages.delete(1.0, END)
        else:
            self.messages.config(state=NORMAL)
            self.messages.delete(1.0, END)
            self.messages.config(state=DISABLED)

    def able(self):
        self.able = True
        self.messages.config(state=NORMAL)

    def disable(self):
        self.able = False
        self.messages.config(state=DISABLED)
