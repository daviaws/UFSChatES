from tkinter import *
from tkinter import messagebox

from communication.communication_protocol import AddContact

class AddContactWindow():
    
    WIDTHPIXELS = 200
    HEIGHTPIXELS = 70   

    def __init__(self, master):
        self.master = master
        self.root = Tk()
        self.root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.center()
        self.root.resizable(0, 0)
        self.root.withdraw()
        self.root.title('Add contact')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        addContactFrame = Frame(self.root, bd=1, relief=SUNKEN)
        addContactFrame.pack(anchor=CENTER, fill=BOTH)
        
        addContactLabel = Label(addContactFrame, text="Add Contact")
        addContactLabel.pack()
        self.addContactEntry = Entry(addContactFrame)
        self.addContactEntry.pack()
        addContactButton = Button(addContactFrame, text='Add', command=self.add_contact)
        addContactButton.pack()

    def add_contact(self):
        cmd = AddContact(username=self.get_entry())
        self.master.update(cmd)

    def already_added(self):
        messagebox.showwarning('Result', 'User already in friend list.', parent=self.root)

    def dont_exist(self):
        messagebox.showwarning('Result', "User don't exist.", parent=self.root)

    def added_self(self):
        messagebox.showerror('Result', 'Cannot add yourself.', parent=self.root)

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