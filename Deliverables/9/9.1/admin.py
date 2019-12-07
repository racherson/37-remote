from ref_wrapper import Ref_Wrapper
from referee import Referee
import socket
from helpers import *


def administrate(player1_wrap, player2_wrap, player1_name, player2_name, player_names):
    player1_wrap.reset_for_new_game()
    player2_wrap.reset_for_new_game()
    print("Setting up new game")
    # register players
    try:
        response = player1_wrap.register()
        if response == GONE_CRAZY:
            print("Could not register player 1")
            return [player2_name], True, player_names
        player_names[player1_name] = response
    except socket.error:
        print("Could not register player 1")
        return [player2_name], True, player_names

    try:
        response = player2_wrap.register()
        if response == GONE_CRAZY:
            print("Could not register player 2")
            return [player1_name], True, player_names
        player_names[player2_name] = response
    except socket.error:
        print("Could not register player 2")
        return [player1_name], True, player_names

    # give players to ref and ask it to play a game
    print("starting game between ", player_names[player1_name], "and ", player_names[player2_name])
    ref = Referee(player1_wrap, player2_wrap, player1_name, player2_name)
    REF_WRAP = Ref_Wrapper(ref)
    winner, illegal = REF_WRAP.play_game()
    if len(winner) == 1:
        print("Winner: ", player_names[winner[0]])
    else:
        print("it was a tie!")

    return winner, illegal, player_names

