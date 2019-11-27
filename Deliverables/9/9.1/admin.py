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
        print("trying to register p1")
        response = player1_wrap.register()
        if response == GONE_CRAZY:
            print("register gone crazy response (player2 auto wins)")
            return [player2_wrap.get_name()], True
    except socket.error:
        print("trying to register p2 since they won! (p1 register socket error")
        player2_wrap.register()
        return [player2_wrap.get_name()]
    try:
        print("trying to register p2")
        response = player2_wrap.register()
        if response == GONE_CRAZY:
            print("register gone crazy response (1 wins)")
            return [player1_wrap.get_name()], True
    except socket.error:
        print("register p2 socket error")
        return [player1_wrap.get_name()]

    # give players to ref and ask it to play a game
    ref = Referee(player1_wrap, player2_wrap)
    REF_WRAP = Ref_Wrapper(ref)
    winner, illegal = REF_WRAP.play_game(player1_wrap, player2_wrap)

    return winner, illegal

