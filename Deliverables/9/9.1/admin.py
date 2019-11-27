from ref_wrapper import Ref_Wrapper
from referee import Referee
import socket
from helpers import *


def administrate(player1_wrap, player2_wrap):
    player1_wrap.reset_for_new_game()
    player2_wrap.reset_for_new_game()
    print("starting game...")
    print("players: ", player1_wrap.get_name(), player2_wrap.get_name())
    # register players
    try:
        response = player1_wrap.register()
        if response == GONE_CRAZY:
            return [player2_wrap.get_name()], True
    except socket.error:
        player2_wrap.register()
        return [player2_wrap.get_name()]
    try:
        response = player2_wrap.register()
        if response == GONE_CRAZY:
            return [player1_wrap.get_name()], True
    except socket.error:
        return [player1_wrap.get_name()]

    # give players to ref and ask it to play a game
    ref = Referee(player1_wrap, player2_wrap)
    REF_WRAP = Ref_Wrapper(ref)
    winner, illegal = REF_WRAP.play_game(player1_wrap, player2_wrap)

    return winner, illegal

