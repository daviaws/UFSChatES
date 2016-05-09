import tkinter as tki # tkinter -> tkinter in Python 3

class GUI(tki.Tk):
    def __init__(self):
        tki.Tk.__init__(self)

        # create a popup menu
        self.aMenu = tki.Menu(self, tearoff=0)
        self.aMenu.add_command(label="Undo", command=self.hello)
        self.aMenu.add_command(label="Redo", command=self.hello)

        # create a frame
        self.aFrame = tki.Frame(self, width=512, height=512)
        self.aFrame.pack()

        # attach popup to frame
        self.listbox = tki.Listbox()
        self.listbox.insert(0, *range(1, 10, 2))
        self.listbox.bind('<3>', lambda e: self.context_menu(e))
        self.listbox.pack()

    def context_menu(self, event):
        widget = event.widget
        index = widget.nearest(event.y)
        _, yoffset, _, height = widget.bbox(index)
        if event.y > height + yoffset + 5: # XXX 5 is a niceness factor :)
            # Outside of widget.
            return
        item = widget.get(index)
        self.listbox.selection_clear(0, tki.END)
        self.listbox.selection_set(index)
        print ("Do something with", index, item)
        self.aMenu.post(event.x_root, event.y_root)

    def hello(self):
        print ("hello!")

gui = GUI()
gui.mainloop()