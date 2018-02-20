import socket
import os
from threading import Thread
import json
#create initializer class, and specify node IP and destination port, specify socket attributes sock_type
#SOCK_RAW can be used for faster RPC calls

class Initializer():

    def __init__(self, device_ip, portname, sock_type = (socket.AF_INET, socket.SOCK_DGRAM)):
        self.device_ip = device_ip
        self.portname = portname
        self.sock_type = sock_type
    
    def getConnection(self):
        sock =  socket.socket(self.sock_type[0], self.sock_type[1])
        sock.connect((self.device_ip, self.portname))
        print('Connected')
        return sock

class PersistantIDStore():

    def __init__(self):
        self.__connected_nodes = []
    
    def add_new(self, node_dict):
        self.__connected_nodes.append(node_dict)
    
    def flush(self):
        with open('Nodes.txt', 'w') as Writer:
            for entries in self.__connected_nodes:
                string_ = "{"
                for key, value in entries.items():
                    string_+="\""+str(key)+"\""+':\"'+str(value)+'\",'
                string_+='\"id\": \"end_entry\"}\n'
                Writer.write(string_)

    def loadFromStorage(self):
        if not os.path.exists('Nodes.txt'):
            print('No file found to read from.')
            return
        with open('Nodes.txt', 'r') as Reader:
            entries = Reader.readlines()
            for entry in entries:
                self.__connected_nodes.append(json.loads(entry))
            return self.__connected_nodes
    
    def clearBuffer(self):
        self.__connected_nodes.clear()

#return an array containing, dicts of type : <node_name, socket>
class ObtainConnectionsForNodes():

    def __init__(self, nodes, socket_type = (socket.AF_INET, socket.SOCK_STREAM)):
        self.nodes = nodes
        self.sock_type = socket_type
    
    def getConnectionPool(self):
        connections = []
        for entry in self.nodes:
            connections.append(
                {
                    'NAME' : entry['Name'],
                    'socket' : Initializer(
                        device_ip = entry['IP'],
                        portname = int(entry['PORT']),
                        sock_type = self.sock_type).getConnection()
                }
            )
        return connections

#Interface to remote shell protocol:
class RemoteShellInterface():

    def __init__(self, socket_, thread = True, mode = 'call'):
        self.socket_ = socket_
        self.thread = thread
    
    def execute(self, command):
        if self.thread:
            print('Starting execution thread, output will be written to : ', 'Output.txt')
            Thread(target = self.__execution, args=(command)).start()
        else:
            data = self.__execution(command)
            return data    

    def __execution(self, *args):
        self.socket_.send(bytes(("Encode_Shell::::"+args[0]).encode('utf-8')))
        response = self.socket_.recv(4096)
        output = str(response.decode('utf-8'))
        if self.thread:
            with open('Output.txt', 'w') as Writer:
                Writer.write(output)
                Writer.close()
                print('Output ready')
        else:
            return output
    
        
def assign_name(socket_, name):
    return {
        'NAME' : name,
        'socket' : socket_
    }

class DispatcherProtocol():

    def __init__(self, socket_, function_metadata):
        self.socket_ = socket_['socket']
        self.function_data = function_metadata
    
    def call(self):

        self.socket_.sendall(
            bytes(("Function_Call::::"+str(self.function_data)).encode('utf-8'))
        )
        data = self.socket_.recv(4096)
        return data
