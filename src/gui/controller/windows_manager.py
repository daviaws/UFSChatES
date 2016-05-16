from gui.windows.chat import ChatWindow

class WindowsManager():

    def __init__(self):
        self.open_windows = {}

    def get_window(self, username):
        if username in self.open_windows:
            return self.open_windows[username]
        else:
            return None

    def open(self, master, username):
        if not username in self.open_windows:
            self.open_windows[username] = ChatWindow(master, username)
        else:
            self.open_windows[username].raises()

    def close(self, username):
        if username in self.open_windows:
            del self.open_windows[username]
