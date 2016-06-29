from tkinter import *
from tkinter import messagebox

from communication.communication_protocol import CreateRoom

class CreateRoomWindow():
    
    WIDTHPIXELS = 200
    HEIGHTPIXELS = 70   

    def __init__(self, master):
        self.master = master
        self.root = Tk()
        self.root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.center()
        self.root.resizable(0, 0)
        self.root.withdraw()
        self.root.title('Create room')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        addContactFrame = Frame(self.root, bd=1, relief=SUNKEN)
        addContactFrame.pack(anchor=CENTER, fill=BOTH)
        
        addContactLabel = Label(addContactFrame, text="Create room")
        addContactLabel.pack()
        self.addContactEntry = Entry(addContactFrame)
        self.addContactEntry.pack()
        addContactButton = Button(addContactFrame, text='Create', command=self.create_room)
        addContactButton.pack()

    def create_room(self):
        cmd = CreateRoom(roomname=self.get_entry())
        self.master.update(cmd)

    def already_exist(self):
        messagebox.showwarning('Result', 'Room already exists.', parent=self.root)

    def usenarme_exist(self):
        messagebox.showwarning('Result', 'Username with same nick already exists.', parent=self.root)

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def get_entry(self):
        entry = self.addContactEntry.get()
        print('Entry is %s' % entry)
        return entry

    def clear(self):
        self.addContactEntry.delete(0, END)

    def on_close(self):
        self.clear()
        self.root.withdraw()

    def raises(self):
        self.on_close()
        self.center()
        self.root.deiconify()