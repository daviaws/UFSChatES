from tkinter import *

class ChatWindow():
    
    WIDTHPIXELS = 200
    HEIGHTPIXELS = 80

    def __init__(self, master):
        self.master = master
        self.root = Tk()
        self.root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.root.resizable(0, 0)
        self.center()
        self.root.withdraw()
        self.root.title('Add contact')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        addContactFrame = Frame(self.root, bd=1, relief=SUNKEN)
        addContactFrame.pack(anchor=CENTER, fill=BOTH)
        
        addContactLabel = Label(addContactFrame, text="Add Contact")
        addContactLabel.pack()
        self.addContactEntry = Entry(addContactFrame)
        self.addContactEntry.pack()
        addContactButton = Button(addContactFrame, text='Add', command= lambda: self.master.update(event_pressed_add_contact, username=self.get_entry()))
        addContactButton.pack()

    def get_entry(self):
        entry = self.addContactEntry.get()
        self.clear()
        print('Entry is %s' % entry)
        return entry

    def center(self):
        self.root.update_idletasks()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def clear(self):
        print('Era pra limpar :c')
        self.addContactEntry.delete(0, END)

    def on_close(self):
        self.clear()
        self.root.withdraw()

    def raises(self):
        self.on_close
        self.center()
        self.root.deiconify()
