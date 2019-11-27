import socket
import json
import pickle
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
            print("exception when trying to register remote player")
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

sock.send(pickle.dumps("establish connection"))
while True:
    try:
        request = pickle.loads(sock.recv(4096))
    except socket.error:
        sock.close()
    print("remote player request", request)
    response = get_response(request)
    print("remote player response", response)
    if response:
        sock.send(pickle.dumps(response))
