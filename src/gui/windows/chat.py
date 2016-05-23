from tkinter import *
from tkinter import messagebox

from gui.widgets.text_box import TextBox
from communication.communication_protocol import Message, CloseChat

class ChatWindow():
    
    WIDTHPIXELS = 1000
    HEIGHTPIXELS = 500

    def __init__(self, master, chating_with):
        self.master = master
        self.root = Tk()
        self.root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.center()
        self.chating_with = chating_with
        self.root.title('Chat with %s' % chating_with)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        logTextFrame = Frame(self.root, bd=1, relief=SUNKEN)
        logTextFrame.pack(anchor=N, fill=BOTH, side=TOP)
        self.logText = TextBox(self.root)

        sendTextFrame = Frame(self.root, bd=1, relief=SUNKEN)
        sendTextFrame.pack(anchor=S, fill=BOTH, side=BOTTOM)
        
        sendTextBox = Frame(sendTextFrame, bd=1, relief=SUNKEN)
        sendTextBox.pack(expand=1, fill=BOTH, side=LEFT)
        self.msgText = TextBox(sendTextBox, NORMAL)

        sendButtonBox = Frame(sendTextFrame, bd=1, relief=SUNKEN)
        sendButtonBox.pack(side=RIGHT)
        sendTextButton = Button(sendButtonBox, text='Send', command=lambda: self.send_message())
        sendTextButton.pack()

    def send_message(self):
        msg = self.msgText.get_text()
        if msg:
            cmd = Message(msg=msg, to=self.chating_with)
            self.master.update(cmd)

    def msg_success(self, user, date):
        self.logText.log('%s - %s: %s' % (date, user, self.msgText.get_text()))
        self.msgText.clean()

    def msg_received(self, date, msg):
        self.logText.log('%s - %s: %s' % (date, self.chating_with, msg))

    def pending_msg(self):
        messagebox.showwarning('Cannot send message', 'Message pendig to %s.' % self.chating_with, parent=self.root)

    def msg_fail(self):
        messagebox.showerror('Message was not sent', 'Fail to send message to %s' % self.chating_with, parent=self.root)

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def on_close(self):
        cmd = CloseChat(username=self.chating_with)
        self.master.update(cmd)
        self.root.destroy()

    def raises(self):
        self.root.withdraw()
        self.root.deiconify()
