import asyncio
from communication import chatserver

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance

coroutine = loop.create_server(chatserver.ServerProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coroutine)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
