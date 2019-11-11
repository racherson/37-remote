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


def try_to_connect(config):
    try:
        sock.connect((config["IP"], config["port"]))
    except Exception:
        try_to_connect(config)


PLAYER_WRAP = Player_Wrapper()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = get_config()
try_to_connect(config)

sock.send(pickle.dumps("establish connection"))
while True:
    request = pickle.loads(sock.recv(4096))
    if request == "close":
        break
    sock.send(pickle.dumps(get_response(request)))
sock.close()
