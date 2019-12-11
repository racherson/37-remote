from player import Player1, Player3
from player_wrapper import Player_Wrapper
import random
import admin
import tournament_admin


print("----------------Testing Game Admin----------------")
for i in range(10):
	p1 = random.randint(0, 1)
	if p1 == 0:
		player1 = Player1("p1")
	else:
		player1 = Player3("p1")

	p1_wrap = Player_Wrapper(player1.name)
	p1_wrap.player = player1
	name1 = p1_wrap.register()

	p2 = random.randint(0, 1)
	if p2 == 0:
		player2 = Player1("p2")
	else:
		player2 = Player3("p2")

	p2_wrap = Player_Wrapper(player2.name)
	p2_wrap.player = player2
	name2 = p2_wrap.register()

	print(admin.administrate(p1_wrap, p2_wrap, name1, name2))

print("----------------Testing Tournament Admin----------------")


def reset_data():
	tournament_admin.curr_default_player_num = 0
	tournament_admin.players = {}
	tournament_admin.rankings = {}
	tournament_admin.beaten = {}
	tournament_admin.player_list = []


print("testing league")

for i in range(10):
	tournament_admin.main("--league", "0")
	reset_data()

print("\n")
print("testing cup")
for i in range(10):
	tournament_admin.main("--cup", "0")
	reset_data()
