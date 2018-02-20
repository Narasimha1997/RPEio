import base64
import marshal
import json
from threading import Thread

'''module to build function from bytecode and dispatch the resulting function as a thread'''

def __buildFunctionFromByteCode(code):
    code = marshal.loads(code)
    return types.FunctionType(code,  globals(), "demo")


def obtainFunctionFromMetaData(meta):
    meta = json.loads(str(meta.decode('utf-8')))
    function_base = meta['function_metadata']
    args = tuple(meta['args'])
    #assume encoding is base64, deocode and build up a function from bytecode:
    clean_byte_code = base64.b64decode(function_base['function'])
    function = __buildFunctionFromByteCode(clean_byte_code)
    return (function, args)

class EventDispatcher(Thread):

    def __init__(self, socket, function, args):

        self.socket = socket
        self.function = function
        self.args = args
    
    def run(self):
        print('Remote execution started')
        return_val = self.function(self.args)
        self.socket.sendall(bytes(return_val.encode('utf-8')))


