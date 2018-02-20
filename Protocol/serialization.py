import marshal
import types
import base64
import json

class SerializationBase():

    def __init__(self, function = None):
        #self.mode = mode
        self.func = function

    def __create_byte_code(self, func = None):
        if func is not None:
            return marshal.dumps(func.__code__)

    def getByteCode(self):
        '''Return byte code from python function'''
        code = self.__create_byte_code(func = self.func)
        return {
            'type' : 'raw',
            'function' : code
        }
    
    def b64String(self):
        code = self.getByteCode()['function']
        return {
           'type' : 'base64',
           'function' : str(base64.b64encode(code).decode())
        }
    
    def b85String(self):
        code = self.__create_byte_code(func = self.func)
        return {
            'type' : 'base85',
            'function' : str(base64.b85encode(code).decode())
        }
    
    def max32BaseString(self, byte_length = 16):
        code = self.__create_byte_code(func = self.func)
        if byte_length == 16:
            return {
                'type' : 'base16',
                'function' : str(base64.b16encode(code).decode())
            }
        return {
            'type' : 'base32',
            'function' : str(base64.b32encode(code).decode())
        }
    
    def asciiString(self):
        code = self.__create_byte_code(self.func)
        return {
            'type' : 'ascii32',
            'function' : str(base64.a85encode(code).decode())
        }
        
def add_arguments(serialized_function, *args):

    return {
        'args' : str(args),
        'function_metadata' : serialized_function
    }

'''uses utf-8 encoding'''
def create_network_portable_stream(function_metadata):
    json_data = json.dumps(function_metadata)
    return bytes(json_data.encode('utf-8'))
    



