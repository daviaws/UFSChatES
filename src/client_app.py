from tkinter import *
import asyncio
from functools import wraps
from communication import chatclient

def runloop(func):
    '''
    This decorator converts a coroutine into a function which, when called,
    runs the underlying coroutine to completion in the asyncio event loop.
    '''
    func = asyncio.coroutine(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = args[0].loop
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper

class MyGui():
    
    def __init__(self):
        self.connection_try = None
        self.loop = asyncio.get_event_loop()
        self.client = chatclient.Client(self.loop, '127.0.0.1', 8888)
        self.root = self.build_gui()

    def build_gui(self):
        root = Tk()
        entry = Entry(root)
        entry.grid()
        Button(root, text='Connect', command= lambda: self.client.send_message(entry.get())).grid()
        return root

    @asyncio.coroutine
    def run_tk(self, root, interval=0.05):
        '''
        Run a tkinter app in an asyncio event loop.
        '''
        try:
            while True:
                self.root.update()
                yield from asyncio.sleep(interval)
        except TclError as e:
            if "application has been destroyed" not in e.args[0]:
                raise
            print('Application closed.')
            self.connection_try.cancel()

    @runloop
    def run(self):
        self.connection_try = asyncio.async(self.client.try_to_connect())
        yield from self.run_tk(self.root)

if __name__ == "__main__":
    gui = MyGui()
    gui.run()