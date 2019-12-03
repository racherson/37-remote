import json
import sys
import importlib
from helpers import *
import remote_player_wrapper
import math
import admin
import random
import socket


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


def update_cup(winner, loser, illegal):
    if illegal:
        rankings[loser] = 0
    rankings[winner[0]] += 1


def scores_to_rankings():
    # need to place player with most points as number 1, etc.
    # https://stackoverflow.com/questions/23641054/adding-a-rank-to-a-dict-in-python
    sorted_by_value = sorted(rankings, key=lambda x: rankings[x], reverse=True)
    rank = 1
    last_value = rankings[sorted_by_value[0]]
    ranked_dict = dict()
    for name in sorted_by_value:
        this_value = rankings[name]
        if this_value != last_value:
            rank += 1
        ranked_dict[name] = rank
        last_value = this_value
    return ranked_dict


num_players = 0
tournament_type = None

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
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((config_data["IP"], config_data["port"]))
module = importlib.import_module(config_data["default-player"])
DefaultPlayer = getattr(module, 'DefaultPlayerWrapper')

# connect remote players
for i in range(num_players):
    sock.listen(30)
    accept_socket, address = sock.accept()
    accept_socket.settimeout(60)
    players.append(remote_player_wrapper.RemotePlayerWrapper(accept_socket))
    name = players[-1].register()
    players[-1].set_name(name)

num_remote = num_players

# add extra default players if needed
while math.log2(num_players) % 1 != 0 or num_players == 1:
    players.append(DefaultPlayer())
    num_players += 1

# name players
rankings = {}
beaten = {}
for i in range(len(players)):
    if i >= num_remote:
        players[i].set_name("default-player-" + str(num_remote-i))
    rankings[players[i].get_name()] = 0
    beaten[players[i].get_name()] = []

# play pair players as determined by tournament type
if tournament_type == LEAGUE:
    for i in range(len(players)):
        for opponent in players[i+1:]:
            winner, loser, illegal = play_game(players[i], opponent)
            update_league(winner, loser, illegal)

elif tournament_type == CUP:
    while len(players) > 1:
        player1 = players[random.randint(0, len(players) - 1)]
        player2 = players[random.randint(0, len(players) - 1)]
        while player2 == player1:
            player2 = players[random.randint(0, len(players) - 1)]
        winner, loser, illegal = play_game(player1, player2)
        update_cup(winner, loser, illegal)
        players.pop(index_of_name(loser))

else:
    pass

# stout the rankings dictionary
sock.shutdown(socket.SHUT_RDWR)
sock.close()
rank_dict = scores_to_rankings()
print("Final Rankings:")
for key, val in rank_dict.items():
    print(val, ": ", key)
