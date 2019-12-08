import socket
import json
from helpers import *
from player import Player1
import random


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
        except:
            print("socket error receive stones gone crazy")
            result = GONE_CRAZY
    elif request[0] == "make-a-move":
        try:
            result = PLAYER_WRAP.make_a_move(request[1])
            print("making a move")
        except socket.error:
            print("make a move gone crazy")
            result = GONE_CRAZY
    elif request[0] == "end-game":
        print("ending game")
        result = "OK"
    else:
        print("invalid request")
        result = GONE_CRAZY
    return result


def try_to_connect(config):
    try:
        sock.connect((config["IP"], config["port"]))
    except socket.error:
        try_to_connect(config)


PLAYER_WRAP = Player1("Rachel" + str(random.randint(0, 10)))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
config = get_config()
try_to_connect(config)
print("connected!")

while True:
    try:
        data = sock.recv(2048)
        if not data:
            break
        incomingJson = data.decode()
        request = json.loads(incomingJson)
        print("request", request[0])
        response = get_response(request)
        print("response", response)
        if response:
            print("sending response")
            sock.send(json.dumps(response).encode())
    except socket.error:
        break

print("closing socket")
sock.close()
