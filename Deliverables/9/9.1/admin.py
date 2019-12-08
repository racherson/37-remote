from ref_wrapper import Ref_Wrapper
from referee import Referee
from helpers import *


def administrate(player1_wrap, player2_wrap, player1_name, player2_name):
    player1_wrap.reset_for_new_game()
    player2_wrap.reset_for_new_game()

    # give players to ref and ask it to play a game
    print("starting game between ", player1_name, "and ", player2_name)
    print("making a ref")
    ref = Referee(player1_wrap, player2_wrap, player1_name, player2_name)
    REF_WRAP = Ref_Wrapper(ref)
    print("calling play game with that ref")
    winner, illegal = REF_WRAP.play_game()
    print("Winner: ", [winner[0]])

    return winner, illegal

