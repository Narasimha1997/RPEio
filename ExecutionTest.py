from Protocol import sender, serialization

socket = sender.Initializer(
    'localhost', 5000
).getConnection()

sock_ = sender.assign_name(socket, "Device_1")

#create a simple function for serailization:

def function(*args):
    import os
    return str(os.listdir())

#serialize:
function_data = serialization.SerializationBase(
    function = function
).b64String()

meta = serialization.add_arguments(function_data, 1, 2, 3, 4)

data = serialization.create_network_portable_stream(meta)

sender.DispatcherProtocol(
    socket_ = sock_, function_metadata = data
).call()
