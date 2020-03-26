# GO Tournament Administrator and Remote Players
An administrator for a GO tournament (9x9 board size) between remote and computer players.

## Setup

    cd final_components
    make

## Use
Remain in the final_components directory for all use.
To run the tournament administrator to start a tournament, you must select a tournament type and the number of remote players to be connected.
The options for tournament type are

    --league
    --cup
The league option is a round-robin tournament where all players play each other.
The rankings are based off of number of wins.

The cup option is a single-elimination tournament where players are eliminated when they lose.
The rankings are decided by how far players make it in the tournament.

To run the tournament, type in terminal:

    ./run <type> <num_remote>
For example:

    ./run --cup 3
After this command, connect that specified number of remote players to the tournament (see Remote Players below).

Once all players have connected, the tournament admin will add computer players to the tournament until the number of players is a power of 2.
Then the admin will run the tournament to completion and print out the final rankings.

## Remote Players
Remote players connect to the tournament admin through TCP sockets.
Our remote players are run through remote_test_driver.py.
To connect a player, in a new terminal type:

    python3 remote_test_driver.py
Run each remote player in a separate terminal window/tab.

In it's current configuration, the remote players connect using "localhost" as the IP in the configuration of go.config.
In order to allow players from multiple computers to connect,
you can change the IP field of go.config to the local IP address of the computer that is running the tournament administrator (./run).
This IP can found from one of the two

    ipconfig
    ifconfig
depending on the machine. All remote players connecting should update their configurations to use the same IP and port as the tournament admin.

As they are, the remote players all use the same computer strategy implemented in player.py in the make_a_move function.
The strategy can be changed and adjusted in this function if desired.

## Testing
Components (referee, player, admin, etc.) were built up in the Deliverables directory, one at a time. As more parts were implemented (higher numbers in Deliverables), some components were altered along the way.
The final version of all components can be found in Deliverables/9/9.1 and in final_components. Unit tests for each component are found in their respective Deliverables folder,
and E2E testing was performed for each on Travis CI.

## Note
The admin and remote players are written in Python3. Depending on your system, you may have to adjust both the run file and how you connect players to  use
py -3 instead of python3.
