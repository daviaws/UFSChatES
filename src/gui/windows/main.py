from tkinter import *

from observers.observer import Observer

class MainWindow(Observer):
    
    HEIGHTPIXELS = 600
    WIDTHPIXELS = 300

    def __init__(self, name, anchor=CENTER):
        super().__init__()
        self.anchor = anchor
        self.name = name

        self.root = self.init_root(name)

    def init_root(self, name):
        root = Tk()
        root.title(name)
        root.geometry('%dx%d' % (self.WIDTHPIXELS, self.HEIGHTPIXELS))
        self.center(root)
        return root

    def get_root(self):
        return self.root

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
