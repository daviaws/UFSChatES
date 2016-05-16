from tkinter import *

from observers.gui_events import event_open_chat_window

class FriendList():

    def __init__(self, master, root):
        self.master = master

        self.listbox = Listbox(root, selectmode=SINGLE)
        self.listbox.pack(expand=True, fill=BOTH)

        self.menu = None
        self.chat = False

        self.listbox.bind('<Double-Button-1>', self.ondoubleclick)
        self.listbox.bind('<<ListboxSelect>>', self.onselect)
        self.listbox.bind('<3>', lambda e: self.context_menu(e))

    def able_chat(self):
        self.chat = True

    def reload(self, friend_list):
        self.listbox.delete(0, END)
        for item in friend_list:
            self.listbox.insert(END, item)

    def ondoubleclick(self, event):
        if self.chat:
            self.chat_contact(self.selection)

    def onselect(self, event):
        self.destroy_menu()
        w = event.widget
        index = int(w.curselection()[0])
        item = w.get(index)
        self.selection = item

    def context_menu(self, event):
        widget = event.widget
        index = widget.nearest(event.y)
        _, yoffset, _, height = widget.bbox(index)
        if event.y > height + yoffset + 5:
            self.destroy_menu()
            return
        item = widget.get(index)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(index)

        self.destroy_menu()
        self.menu = Menu(self.listbox, tearoff=0)
        if self.chat:
            self.menu.add_command(label="Chat with '%s'" % (item), command= lambda: self.chat_contact(item))
        self.menu.add_command(label="Remove '%s'" % (item), command= lambda: self.remove_contact(item))
        self.menu.add_separator()
        self.menu.add_command(label="Exit menu", command=self.destroy_menu)
        self.menu.post(event.x_root, event.y_root)

    def chat_contact(self, contact):
        self.master.update(event_open_chat_window, username=contact)

    def remove_contact(self, contact):
        print ("Remove '%s'" % (contact))

    def destroy_menu(self):
        if self.menu:
            self.menu.unpost()
            self.menu = None