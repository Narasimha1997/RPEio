from subprocess import check_output
import socket
from threading import Thread
from Protocol import dispatcher
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_server.bind(('localhost', 5000))
sock_server.listen(3)

def executeAsThread(**kwargs):
    output = check_output(
        kwargs['command'], shell = True
    )
    socket_ = kwargs['socket']
    socket_.sendall(bytes(output))
    socket_.close()

while True:
    connection_s , client_addr = sock_server.accept()
    data_bytes = connection_s.recv(8988)
    print(data_bytes)
    command = str(data_bytes.decode('utf-8')).split('::::')
    if command[0] == 'Encode_Shell':
        Thread(target=executeAsThread, kwargs={
            "command" : command[1], "socket" : connection_s
        }).start()
    elif command[0] == 'Function_Call':
        function, args = dispatcher.obtainFunctionFromMetaData(meta = bytes(command[1].encode()))
        dispatcher.EventDispatcher(socket = connection_s, function = function, args = args).start()
