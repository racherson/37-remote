import socket
import json
import pickle
from player_wrapper import Player_Wrapper


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


def get_response(request):
    if request[0] == "register":
        return PLAYER_WRAP.register()
    if request[0] == "receive-stones":
        return PLAYER_WRAP.receive_stones(request[1])
    if request[0] == "make-a-move":
        return PLAYER_WRAP.make_a_move(request[1])
    raise Exception("Invalid request")


PLAYER_WRAP = Player_Wrapper()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = get_config()
sock.bind((config["IP"], config["port"]))
sock.listen(5)

while True:
    # receives data from client socket
    acceptSocket, address = sock.accept()
    request_data = acceptSocket.recv(1024)
    request = pickle.loads(request_data)

    # sends response generated from request and closes client socket
    acceptSocket.send(pickle.dumps(get_response(request)))
    acceptSocket.close()

sock.close()
