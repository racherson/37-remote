import json
import sys
import importlib
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
    arr = [player1.get_name(), player2.get_name()]
    return [arr[random.randint(0, 1)]]


def get_loser(player1, player2, winner):
    if winner == player1.get_name():
        return player2
    return player1


def index_of_name(name):
    for i in range(len(players)):
        if players[i].get_name() == name:
            return i


def create_default_player(name):
    default_player = DefaultPlayer()
    default_player.register()
    default_player.set_name(name)
    return default_player


# give players to admin to play a game
def play_game(player, opponent):
    winner, illegal = admin.administrate(player, opponent)
    if len(winner) == 2:
        winner = flip_coin(player, opponent)
    loser = get_loser(player, opponent, winner[0]).get_name()
    return winner, loser, illegal


def update_league(winner, loser, illegal):
    if illegal:
        rankings[loser] = 0
        default_player = create_default_player(loser)
        players[index_of_name(loser)] = default_player
        # distribute points of loser
        for player_name in beaten[loser]:
            rankings[player_name] += 1
        beaten[loser] = []
    else:
        beaten[winner[0]].append(loser)
    rankings[winner[0]] += 1
    return loser


def update_cup(winner, loser, illegal):
    if illegal:
        rankings[loser] = -1
        default_player = create_default_player(loser)
        players[index_of_name(loser)] = default_player
    if rankings[winner[0]] != -1:
        rankings[winner[0]] += 1  # TODO: VERY DIFFERENT RANKINGS FOR CUP TOURNEY?
    return loser


def scores_to_rankings():
    # need to place player with most points as number 1, etc.
    pass


# get args from command line
if sys.argv[1] == LEAGUE:
    tournament_type = LEAGUE
elif sys.argv[1] == CUP:
    tournament_type = CUP
else:
    tournament_type = LEAGUE

num_players = int(sys.argv[2])
players = []

# make socket
config_data = get_config()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((config_data["IP"], config_data["port"]))
module = importlib.import_module(config_data["default-player"])
DefaultPlayer = getattr(module, 'DefaultPlayerWrapper')

# connect remote players
for i in range(num_players):
    sock.listen(5)
    accept_socket, address = sock.accept()
    accept_socket.settimeout(30)
    players.append(remote_player_wrapper.RemotePlayerWrapper(accept_socket))

# add extra default players if needed
while math.log2(num_players) % 1 != 0 or num_players == 1:
    players.append(DefaultPlayer())
    num_players += 1

# name players
rankings = {}
beaten = {}
for i in range(len(players)):
    players[i].set_name(str(i))
    rankings[players[i].get_name()] = 0
    beaten[players[i].get_name()] = []

# play pair players as determined by tournament type
if tournament_type == LEAGUE:
    for i in range(len(players)):
        for opponent in players[i+1:]:
            print(i, opponent.get_name())
            winner, loser, illegal = play_game(players[i], opponent)
            update_league(winner, loser, illegal)
            print("now players are ", players)
            print("now rankings are ", rankings)

elif tournament_type == CUP:
    while len(players) > 1:
        player1 = players[random.randint(0, len(players) - 1)]
        player2 = players[random.randint(0, len(players) - 1)]
        while player2 == player1:
            player2 = players[random.randint(0, len(players) - 1)]
        winner, loser, illegal = play_game(player1, player2)
        update_cup(winner, loser, illegal)
        players.pop(index_of_name(loser))
        print("now players are ", players)
        print("now rankings are ", rankings)

else:
    pass

# stout the rankings dictionary
sock.close()
print(json.dumps(rankings, separators=(',', ':')))
