from communication import chatserver

server = chatserver.Server('127.0.0.1', 8888)
server.run()
