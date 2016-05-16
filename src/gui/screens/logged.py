from tkinter import *

from observers.gui_events import event_popup_add_contact
from gui.widgets.friend_list import FriendList

class LoggedScreen():

    def __init__(self, master, root, anchor=CENTER):

        self.master = master
        self.mainFrame = Frame(root, bd=1, relief=SUNKEN)

        loggedFrame = Frame(self.mainFrame, bd=1, relief=SUNKEN)
        loggedFrame.pack(expand=True, fill=BOTH)

        login = Button(loggedFrame, text='Add contact', command= lambda: self.master.update(event_popup_add_contact))
        login.pack()

        onlineFrame = Frame(loggedFrame, bd=1, relief=SUNKEN)
        onlineFrame.pack(expand=True, fill=BOTH)
        onlineFriendsLabel = Label(onlineFrame, text="Online Friends")
        onlineFriendsLabel.pack()
        self.onlineFriends = FriendList(master, onlineFrame)
        self.onlineFriends.able_chat()
        self.onlineFriends.reload(['one', 'two', 'three'])

        offlineFrame = Frame(loggedFrame, bd=1, relief=SUNKEN)
        offlineFrame.pack(expand=True, fill=BOTH)
        offlineFriendsLabel = Label(offlineFrame, text="Offline Friends")
        offlineFriendsLabel.pack()
        self.offlineFriends = FriendList(master, offlineFrame)
        self.offlineFriends.reload(['four', 'five', 'six'])

        logout = Button(loggedFrame, text='Logout', command= lambda: print('logout'))
        logout.pack()

    def raises(self):
        self.mainFrame.pack(expand=True, fill=BOTH)

    def fall(self):
        self.mainFrame.pack_forget()