import json
import sys
from ref_wrapper import Ref_Wrapper
from referee import Referee
import socket


def administrate(player1_wrap, player2_wrap):
    # register players
    try:
        player1_wrap.register()
    except socket.error:
        player2_wrap.register()
        print(json.dumps([player2_wrap.get_name()]))
        sys.exit()
    player2_wrap.register()

    # give players to ref and ask it to play a game
    ref = Referee(player1_wrap, player2_wrap)
    REF_WRAP = Ref_Wrapper(ref)
    winner, illegal = REF_WRAP.play_game("remote", "default")

    # close up sockets
    try:
        player1_wrap.close()
    except socket.error:
        return winner, illegal

    try:
        player1_wrap.sock.close()
        return winner, illegal
    except socket.error:
        return winner, illegal

