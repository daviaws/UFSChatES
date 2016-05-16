from tkinter import *

from gui.widgets.text_box import TextBox
from observers.gui_events import event_send_message_client, event_closed_chat_window

class ChatWindow():
    
    WIDTHPIXELS = 200
    HEIGHTPIXELS = 80

    def __init__(self, master, chating_with):
        self.master = master
        self.root = Tk()
        self.root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.root.resizable(0, 0)
        self.center()
        self.root.withdraw()
        self.chating_with = chating_with
        self.root.title('Chat with %s' % chating_with)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.pending_message = False

        logTextFrame = Frame(self.root, bd=1, relief=SUNKEN)
        logTextFrame.pack(anchor=N, fill=BOTH)
        self.logText = TextBox(logTextFrame)

        sendTextFrame = Frame(self.root, bd=1, relief=SUNKEN)
        sendTextFrame.pack(anchor=S, fill=BOTH)
        self.msgText = TextBox(sendTextFrame, NORMAL)
        sendTextButton = Button(sendTextFrame, anchor=E, text='Send', command= lambda: self.send_message())
        sendTextButton.pack()

    def send_message():
        if pending_message:
            tkMessageBox.showwarning('Message pendig to %s.' % self.chating_with)
        else:
            self.pending_message = True
            self.master.update(event_send_message_client, msg=self.msgText.get_text(), to=self.chating_with)

    def msg_success(self):
        self.pending_message = False
        self.logText.log('You: %s' % self.msgText.get_text())
        self.logText.clean()

    def msg_received(self, msg):
        self.pending_message = False
        self.logText.log('%s: %s' % (self.chating_with, msg))

    def msg_fail(self):
        self.pending_message = False
        tkMessageBox.showerror('Fail to send message to %s' % self.chating_with)

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def on_close(self):
        self.master.update(event_closed_chat_window, username=self.chating_with)
        self.root.destroy()

    def raises(self):
        self.on_close
        self.center()
        self.root.deiconify()
