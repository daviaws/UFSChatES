from tkinter import *
import asyncio
from functools import wraps
import chatclient

# def runloop(func):
#     '''
#     This decorator converts a coroutine into a function which, when called,
#     runs the underlying coroutine to completion in the asyncio event loop.
#     '''
#     func = asyncio.coroutine(func)
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         return asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))
#     return wrapper

@asyncio.coroutine
def run_tk(root, interval=0.05):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            root.update()
            yield from asyncio.sleep(interval)
    except TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise

def main(loop):
    root = Tk()
    entry = Entry(root)
    entry.grid()
    
    client = chatclient.Client(loop, '127.0.0.1', 8888)
    asyncio.async(client.try_to_connect())
    Button(root, text='Connect', command= lambda: client.send_message(entry.get())).grid()
    
    yield from run_tk(root)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))