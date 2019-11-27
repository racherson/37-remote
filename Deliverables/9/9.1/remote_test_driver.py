import socket
import json
# import pickle
from helpers import *
from player import Player1


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


def get_response(request):
    if request[0] == "register":
        try:
            result = PLAYER_WRAP.register()
        except:
            result = GONE_CRAZY
    elif request[0] == "receive-stones":
        try:
            result = PLAYER_WRAP.receive_stones(request[1])
        except socket.error:
            result = GONE_CRAZY
    elif request[0] == "make-a-move":
        try:
            result = PLAYER_WRAP.make_a_move(request[1])
        except socket.error:
            result = GONE_CRAZY
    elif request[0] == "end-game":
        result = "OK"
    else:
        result = GONE_CRAZY
    return result


def try_to_connect(config):
    try:
        sock.connect((config["IP"], config["port"]))
    except socket.error:
        try_to_connect(config)


PLAYER_WRAP = Player1()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = get_config()
try_to_connect(config)

sock.send("establish connection".encode())
while True:
    request = None
    try:
        request = sock.recv(4096).decode()
    except:
        break
    response = get_response(request)
    if response:
        sock.send(response.encode())
