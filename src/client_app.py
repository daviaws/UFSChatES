from gui.controllers.controller import Controller

APP_NAME = 'UFSChat'

ip = '127.0.0.1'
port = 8888
if __name__ == "__main__":
    gui = Controller(APP_NAME, ip, port)
    gui.run()
