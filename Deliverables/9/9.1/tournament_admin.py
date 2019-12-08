import json
import sys
import importlib
from helpers import *
import remote_player_wrapper
import math
import admin
import random
import socket


curr_default_player_num = 0


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


def add_player_to_tournament(player, name, replacement):
    print("adding player to data structures")
    players[name] = player
    rankings[name] = 0
    beaten[name] = []
    if not replacement:
        player_list.append(name)


def setup_from_config():
    config_data = get_config()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((config_data["IP"], config_data["port"]))

    module = importlib.import_module(config_data["default-player"])
    DefaultPlayer = getattr(module, 'DefaultPlayerWrapper')
    return sock, DefaultPlayer


def flip_coin(player1, player2):
    arr = [player1, player2]
    return [arr[random.randint(0, 1)]]


def get_loser(player1, player2, winner):
    if winner == player1:
        return player2
    return player1


def create_default_player(cheater):
    global curr_default_player_num
    if cheater:
        name = "replacement-default-player-" + str(curr_default_player_num)
    else:
        name = "default-player-" + str(curr_default_player_num)
    default_player = DefaultPlayer(name)
    curr_default_player_num += 1
    return default_player, name


# give players to admin to play a game
def play_game(player, opponent, p_name, o_name):
    winner, illegal = admin.administrate(player, opponent, p_name, o_name)
    if len(winner) == 2:
        winner = flip_coin(p_name, o_name)
    loser = get_loser(p_name, o_name, winner[0])
    return winner, loser, illegal


def update_league(winner, loser, illegal):
    if illegal:
        rankings[loser] = 0
        default_player, name = create_default_player(cheater=True)
        # replace internal player name in player list
        player_list[player_list.index(loser)] = name
        # put the replacement player in all other data structures
        add_player_to_tournament(default_player, name, replacement=True)
        # distribute points of loser
        for player_name in beaten[loser]:
            rankings[player_name] += 1
        beaten[loser] = []
    else:
        # only add non cheaters so we don't give back points to any cheaters
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
else:
    raise InvalidTournamentType("Invalid tournament type.")

num_players = int(sys.argv[2])

# create data structures for player data
players = {}  # dictionary mapping player name to player objects
rankings = {}  # mapping player names to scores
beaten = {}  # mapping player names to names of players beaten
player_list = []  # list of active players

# make socket
sock, DefaultPlayer = setup_from_config()

# connect remote players
for i in range(num_players):
    sock.listen(10)
    accept_socket, address = sock.accept()
    print("server accepted a socket")
    accept_socket.settimeout(30)
    new_player = remote_player_wrapper.RemotePlayerWrapper(accept_socket)
    print("new remote player wrapper")
    try:
        new_player_name = new_player.register()
        print("new player name", new_player_name)
        if new_player_name == GONE_CRAZY:
            print("remote player gone crazy")
            new_player, new_player_name = create_default_player(cheater=False)
    except socket.error:
        print("remote player socket error")
        new_player, new_player_name = create_default_player(cheater=False)
    add_player_to_tournament(new_player, new_player_name, replacement=False)

num_remote = num_players

# add extra default players if needed
while math.log2(num_players) % 1 != 0 or num_players == 1:
    new_player, new_name = create_default_player(cheater=False)
    print("new default player")
    new_player.register()
    print("default player registered")
    add_player_to_tournament(new_player, new_name, replacement=False)
    num_players += 1

print("player_list", player_list)

# play pair players as determined by tournament type
if tournament_type == LEAGUE:
    print("league tourney")
    for i in range(len(player_list)):
        for opponent in player_list[i+1:]:
            winner, loser, illegal = play_game(players[player_list[i]], players[opponent], player_list[i], opponent)
            update_league(winner, loser, illegal)

elif tournament_type == CUP:
    while len(player_list) > 1:
        player1 = player_list[0]
        player2 = player_list[1]
        winner, loser, illegal = play_game(players[player1], players[player2], player1, player2)
        update_cup(winner, loser, illegal)
        player_list.remove(loser)


# stout the rankings dictionary
print("close socket")
sock.close()
rank_dict = scores_to_rankings()
print("Final Rankings:")
for key, val in rank_dict.items():
    print(key, ": ", val)
