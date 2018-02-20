from Protocol import sender
import socket

ID = sender.PersistantIDStore().loadFromStorage()

pool = sender.ObtainConnectionsForNodes(
    nodes = ID, socket_type = (socket.AF_INET, socket.SOCK_STREAM)
).getConnectionPool()
print('Connection established')
command = input('Enter command:\t')
for sockets in pool:
    output = sender.RemoteShellInterface(
            socket_ = sockets['socket'], thread = False, mode = 'call'
        ).execute(command)
    print(output)