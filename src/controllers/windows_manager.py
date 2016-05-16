from gui.windows.chat import ChatWindow

class WindowsManager():

    def __init__(self):
        self.open_windows = {}

    def is_opened(self, username):
        if username in self.open_windows:
            return True
        return False

    def open(self, master, username):
        if not username in self.open_windows:
            self.open_windows[username] = ChatWindow(master, username)

    def close(self, username)
        if username in self.open_windows:
            del self.open_windows[username]
