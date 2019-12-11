from player import Player1, Player3
from player_wrapper import Player_Wrapper
import random
import admin
import tournament_admin

for i in range(100):
	p1 = random.randint(0,1)
	if p1 == 0:
		player1 = Player1("p1")
	else:
		player1 = Player3("p1")

	p1_wrap = Player_Wrapper(player1.name)
	p1_wrap.player = player1

	p2 = random.randint(0,1)
	if p2 == 0:
		player2 = Player1("p2")
	else:
		player2 = Player3("p2")

	p2_wrap = Player_Wrapper(player2.name)
	p2_wrap.player = player2

	print(admin.administrate(p1_wrap,p2_wrap,"p1","p2", {"p1":"p1", "p2":"p2"}))

