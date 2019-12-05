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
curr_default_player_num = 0


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


def flip_coin(player1_name, player2_name):
    arr = [player1_name, player2_name]
    return [arr[random.randint(0, 1)]]


def get_loser(player1, player2, winner):
    if winner == player1:
        return player2
    return player1


def create_default_player(name):
    default_player = DefaultPlayer(name)
    return default_player


# give players to admin to play a game
def play_game(player, opponent, p_name, o_name):
    winner, illegal = admin.administrate(player, opponent, p_name, o_name)
    if len(winner) == 2:
        winner = flip_coin(p_name, o_name)
    loser = get_loser(p_name, o_name, winner[0])
    return winner, loser, illegal


def update_league(winner, loser, illegal):
    global curr_default_player_num
    if illegal:
        rankings[loser] = 0
        default_player = create_default_player("replacement-default-player-" + str(curr_default_player_num))
        curr_default_player_num += 1
        players[loser] = default_player
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
    sorted_by_value = sorted(rankings, key=lambda x: rankings[x], reverse=True)
    rank = 1
    last_value = rankings[sorted_by_value[0]]
    ranked_dict = dict()
    for name in sorted_by_value:
        this_value = rankings[name]
        if this_value != last_value:
            rank += 1
        if rank in ranked_dict:
            ranked_dict[rank].append(name)
        else:
            ranked_dict[rank] = [name]
        last_value = this_value
    return ranked_dict


# get args from command line
if sys.argv[1] == LEAGUE:
    tournament_type = LEAGUE
elif sys.argv[1] == CUP:
    tournament_type = CUP
else:  # default
    tournament_type = LEAGUE

num_players = int(sys.argv[2])
# players is a dictionary mapping player name to player objects
players = {}

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
    new_player = remote_player_wrapper.RemotePlayerWrapper(accept_socket)
    players[new_player.register()] = new_player

num_remote = num_players

# add extra default players if needed
while math.log2(num_players) % 1 != 0 or num_players == 1:
    new_player = create_default_player("default-player-" + str(curr_default_player_num))
    players[new_player.register()] = new_player
    num_players += 1

rankings = {}
beaten = {}
for player in players:
    rankings[player] = 0
    beaten[player] = []

# play pair players as determined by tournament type
if tournament_type == LEAGUE:
    player_list = list(players.keys())
    for i in range(len(player_list)):
        for opponent in player_list[i+1:]:
            winner, loser, illegal = play_game(players[player_list[i]], players[opponent], player_list[i], opponent)
            update_league(winner, loser, illegal)

elif tournament_type == CUP:
    player_list = list(players.keys())
    while len(player_list) > 1:
        print(len(player_list))
        player1 = player_list[0]
        player2 = player_list[1]
        # while player2 == player1:
        #     player2 = player_list[random.randint(0, len(player_list) - 1)]
        winner, loser, illegal = play_game(players[player1], players[player2], player1, player2)
        update_cup(winner, loser, illegal)
        player_list.remove(loser)

else:
    pass

# stout the rankings dictionary
sock.close()
rank_dict = scores_to_rankings()
print("Final Rankings:")
for key, val in rank_dict.items():
    print(key, ": ", val)
