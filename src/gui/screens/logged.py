from tkinter import *

from communication.communication_protocol import PopupAddContact
from gui.widgets.friend_list import FriendList

class LoggedScreen():

    def __init__(self, master, root, anchor=CENTER):

        self.master = master
        self.mainFrame = Frame(root, bd=1, relief=SUNKEN)

        loggedFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        loggedFrame.pack(expand=True, fill=BOTH)

        addContact = Button(loggedFrame, text='Add contact', command= lambda: self.master.update(PopupAddContact()))
        addContact.pack(anchor=N)

        createRoom = Button(loggedFrame, text='Create room', command= lambda: self.master.update(PopupAddContact()))
        createRoom.pack(anchor=S)

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
        self.yourRooms = FriendList(master, inFrame)
        
        outFrame = Frame(roomFrame, bd=1, relief=SUNKEN)
        outFrame.pack(expand=True, fill=BOTH)
        outRoomsLabel = Label(outFrame, text="Public rooms")
        outRoomsLabel.pack()
        self.publicRooms = FriendList(master, outFrame)

        logout = Button(root, text='Logout', command= lambda: print('logout'))
        logout.pack(side=BOTTOM)

    def reload_lists(self, online, offline):
        self.onlineFriends.reload(online)
        self.offlineFriends.reload(offline)

    def raises(self):
        self.mainFrame.pack(expand=True, fill=BOTH)

    def fall(self):
        self.mainFrame.pack_forget()