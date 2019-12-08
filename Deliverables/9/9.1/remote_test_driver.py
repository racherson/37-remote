import socket
import json
from helpers import *
from player import Player1


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


def get_response(request):
    if request[0] == "register":
        try:
            print("registering...")
            result = PLAYER_WRAP.register()
        except:
            print("register gone crazy")
            result = GONE_CRAZY
    elif request[0] == "receive-stones":
        try:
            print("receiving stones:", request[1])
            result = PLAYER_WRAP.receive_stones(request[1])
        except socket.error:
            print("receive stones gone crazy")
            result = GONE_CRAZY
    elif request[0] == "make-a-move":
        try:
            result = PLAYER_WRAP.make_a_move(request[1])
            print("making a move: ", result)
        except socket.error:
            print("make a move gone crazy")
            result = GONE_CRAZY
    elif request[0] == "end-game":
        print("ending game")
        result = "OK"
    else:
        print("request gone crazy??")
        result = GONE_CRAZY
    return result


def try_to_connect(config):
    try:
        sock.connect((config["IP"], config["port"]))
    except socket.error:
        try_to_connect(config)


PLAYER_WRAP = Player1("Rachel")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = get_config()
print("trying to connect")
try_to_connect(config)
print("connected!")

while True:
    try:
        request = json.loads(sock.recv(recv_size).decode())
        print("request", request)
        response = get_response(request)
        print("response", response)
        if response:
            print("sending response")
            sock.send(json.dumps(response).encode())
    except json.decoder.JSONDecodeError:
        pass
    except socket.error:
        print("error")
        break

