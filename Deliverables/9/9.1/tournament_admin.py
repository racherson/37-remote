import json
import sys
from importlib.machinery import SourceFileLoader
from helpers import *
import remote_player_wrapper
import math
import admin
import random
import socket


num_players = 0
tournament_type = None


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


def flip_coin(player1, player2):
    arr = [player1, player2]
    return arr[random.randint(0, 1)]


def get_loser(player1, player2, winner):
    if winner == player1.get_name():
        return player2
    return player1


def index_of_name(name):
    for i in range(len(players)):
        if players[i].get_name() == name:
            return i


# give players to administrator, get winner, update rankings
def play_and_update(player, opponent):
    winner, illegal = admin.administrate(player, opponent)
    print(winner, illegal)
    if len(winner) == 2:
        winner = flip_coin(player, opponent)
    if illegal:
        cheater_name = get_loser(player, opponent, winner[0]).get_name()
        rankings[cheater_name] = -1
        default_player = defaultFile.default_player
        default_player.register()
        default_player.set_name(cheater_name)
        print("default new name:", default_player.get_name())
        players[index_of_name(cheater_name)] = default_player
    print("winner:", winner[0])
    if rankings[winner[0]] != -1:
        rankings[winner[0]] += 1
    return get_loser(player, opponent, winner)


# get args from command line
if sys.argv[1] == LEAGUE:
    tournament_type = LEAGUE
elif sys.argv[1] == CUP:
    tournament_type = CUP
else:
    tournament_type = None

num_players = int(sys.argv[2])
players = []

# make socket
config_data = get_config()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((config_data["IP"], config_data["port"]))

# connect remote players
for i in range(num_players):
    sock.listen(5)
    accept_socket, address = sock.accept()
    accept_socket.settimeout(30)
    players.append(remote_player_wrapper.RemotePlayerWrapper(accept_socket))

defaultFile = SourceFileLoader("default_player", config_data["default-player"]).load_module()

# add extra default players if needed
while math.log2(num_players) % 1 != 0 or num_players == 1:
    players.append(defaultFile.default_player)
    num_players += 1
print(players)

# name players
rankings = {}
for i in range(len(players)):
    players[i].set_name(str(i))
    rankings[players[i].get_name()] = 0
print(rankings)


if tournament_type == LEAGUE:
    for i in range(len(players)):
        for opponent in players[i+1:]:
            print(len(players))
            print("current players:", players[i].get_name(), opponent.get_name())
            play_and_update(players[i], opponent)

elif tournament_type == CUP:
    while len(players) > 1:
        player1 = players[random.randint(0, len(players) - 1)]
        player2 = players[random.randint(0, len(players) - 1)]
        while player2 == player1:
            player2 = players[random.randint(0, len(players) - 1)]
        loser = play_and_update(player1, player2)
        loser_name = loser.get_name()
        players.pop(index_of_name(loser_name))

else:
    raise Exception("Invalid tournament type")

# stout the rankings dictionary
sock.close()
print(json.dumps(rankings, separators=(',', ':')))
