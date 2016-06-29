from tkinter import *

from communication.communication_protocol import PopupAddContact, PopupCreateRoom
from gui.widgets.friend_list import FriendList
from gui.widgets.room_list import RoomList

class LoggedScreen():

    def __init__(self, master, root, anchor=CENTER):

        self.master = master
        self.mainFrame = Frame(root, bd=1, relief=SUNKEN)

        loggedFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        loggedFrame.pack(expand=True, fill=BOTH)

        addContact = Button(loggedFrame, text='Add contact', command= lambda: self.master.update(PopupAddContact()))
        addContact.pack(anchor=N)

        createRoom = Button(loggedFrame, text='Create room', command= lambda: self.master.update(PopupCreateRoom()))
        createRoom.pack(anchor=S)

        logout = Button(loggedFrame, text='Logout', command= lambda: print('logout'))
        logout.pack(side=BOTTOM)

        contactFrame = Frame(loggedFrame, bd=1, relief=SUNKEN)
        contactFrame.pack(expand=True, fill=BOTH, side=RIGHT)
        
        onlineFrame = Frame(contactFrame, bd=1, relief=SUNKEN)
        onlineFrame.pack(expand=True, fill=BOTH)
        onlineFriendsLabel = Label(onlineFrame, text="Online Friends")
        onlineFriendsLabel.pack()
        self.onlineFriends = FriendList(master, onlineFrame)
        self.onlineFriends.able_chat()
        
        offlineFrame = Frame(contactFrame, bd=1, relief=SUNKEN)
        offlineFrame.pack(expand=True, fill=BOTH)
        offlineFriendsLabel = Label(offlineFrame, text="Offline Friends")
        offlineFriendsLabel.pack()
        self.offlineFriends = FriendList(master, offlineFrame)

        roomFrame = Frame(loggedFrame, bd=1, relief=SUNKEN)
        roomFrame.pack(expand=True, fill=BOTH, side=LEFT)
        
        inFrame = Frame(roomFrame, bd=1, relief=SUNKEN)
        inFrame.pack(expand=True, fill=BOTH)
        inRoomsLabel = Label(inFrame, text="Your rooms")
        inRoomsLabel.pack()
        self.yourRooms = RoomList(master, inFrame)
        self.yourRooms.able_chat()
        
        outFrame = Frame(roomFrame, bd=1, relief=SUNKEN)
        outFrame.pack(expand=True, fill=BOTH)
        outRoomsLabel = Label(outFrame, text="Public rooms")
        outRoomsLabel.pack()
        self.publicRooms = RoomList(master, outFrame)

    def reload_lists(self, online_contacts, offline_contacts, your_rooms, public_rooms):
        self.onlineFriends.reload(online_contacts)
        self.offlineFriends.reload(offline_contacts)
        self.yourRooms.reload(your_rooms)
        self.publicRooms.reload(public_rooms)

    def raises(self):
        self.mainFrame.pack(expand=True, fill=BOTH)

    def fall(self):
        self.mainFrame.pack_forget()