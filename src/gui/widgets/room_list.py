from tkinter import *

from communication.communication_protocol import OpenChat, JoinRoom, LeaveRoom
#from observers.gui_events import event_open_chat_window

class RoomList():

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

    def reload(self, room_list):
        self.listbox.delete(0, END)
        for item in room_list:
            self.listbox.insert(END, item)

    def ondoubleclick(self, event):
        if self.selection:
            if self.chat:
                self.chat_room(self.selection)

    def onselect(self, event):
        self.destroy_menu()
        w = event.widget
        if w.curselection():
            index = int(w.curselection()[0])
            item = w.get(index)
        else:
            item = None
        self.selection = item

    def context_menu(self, event):
        widget = event.widget
        try:
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
                self.menu.add_command(label="Chat with '%s'" % (item), command= lambda: self.chat_room(item))
                self.menu.add_command(label="Exit room '%s'" % (item), command= lambda: self.exit_room(item))
            else:
                self.menu.add_command(label="Enter room '%s'" % (item), command= lambda: self.enter_room(item))
            self.menu.add_separator()
            self.menu.add_command(label="Exit menu", command=self.destroy_menu)
            self.menu.post(event.x_root, event.y_root)
        except:
            pass

    def chat_room(self, room):
        cmd = OpenChat(username=room)
        self.master.update(cmd)

    def enter_room(self, room):
        cmd = JoinRoom(roomname=room)
        self.master.update(cmd)

    def exit_room(self, room):
        cmd = LeaveRoom(roomname=room)
        self.master.update(cmd)        

    def destroy_menu(self):
        if self.menu:
            self.menu.unpost()
            self.menu = None
