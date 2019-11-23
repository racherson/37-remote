from ref_wrapper import Ref_Wrapper
from referee import Referee
import socket


def administrate(player1_wrap, player2_wrap):
    print("starting game...")
    print("player1", player1_wrap.get_name())
    print("player2", player2_wrap.get_name())
    # register players
    try:
        player1_wrap.register()
    except socket.error:
        player2_wrap.register()
        return [player2_wrap.get_name()]
    try:
        player2_wrap.register()
    except socket.error:
        return [player1_wrap.get_name()]

    # give players to ref and ask it to play a game
    ref = Referee(player1_wrap, player2_wrap)
    REF_WRAP = Ref_Wrapper(ref)
    winner, illegal = REF_WRAP.play_game(player1_wrap, player2_wrap)
    print("admin winner", winner, illegal)

    return winner, illegal

