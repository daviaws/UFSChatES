from tkinter import *

class TextBox():

    def __init__(self, root, state=DISABLED):
        if state == DISABLED:
            self.able = False
        elif state == NORMAL:
            self.able = True
        consoleFrame = Frame(root)
        consoleFrame.pack(expand=1, fill=BOTH)
        scrollbar = Scrollbar(consoleFrame)
        scrollbar.pack(fill=Y, side=RIGHT)
        self.messages = Text(consoleFrame, background='white', bd=2, relief=SUNKEN, state=state, yscrollcommand=scrollbar.set)
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
        text = self.messages.get("1.0",END)
        text = text[:-1]
        return text

    def clean(self):
        if self.able:
            self.messages.delete(1.0, END)
        else:
            self.messages.config(state=NORMAL)
            self.messages.delete(1.0, END)
            self.messages.config(state=DISABLED)

    def enable(self):
        self.able = True
        self.messages.config(state=NORMAL)

    def disable(self):
        self.able = False
        self.messages.config(state=DISABLED)
