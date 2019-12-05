from ref_wrapper import Ref_Wrapper
from referee import Referee
import socket
from helpers import *


def administrate(player1_wrap, player2_wrap, player1_name, player2_name, player_dict):
    player1_wrap.reset_for_new_game()
    player2_wrap.reset_for_new_game()
    # register players
    try:
        print("registering player1")
        response = player1_wrap.register()
        if response == GONE_CRAZY:
            print("player1 register is gone crazy")
            return [player2_name], True
        player_dict[response] = player_dict.pop(player1_name)
    except socket.error:
        return [player2_name]

    try:
        print("registering player2")
        response = player2_wrap.register()
        if response == GONE_CRAZY:
            return [player1_name], True
        player_dict[response] = player_dict.pop(player2_name)
    except socket.error:
        return [player1_name]

    # give players to ref and ask it to play a game
    ref = Referee(player1_wrap, player2_wrap, player1_name, player2_name)
    REF_WRAP = Ref_Wrapper(ref)
    winner, illegal = REF_WRAP.play_game()
    print("winner", winner)

    return winner, illegal, player_dict

