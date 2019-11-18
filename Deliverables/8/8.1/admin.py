import json
import sys
from importlib.machinery import SourceFileLoader
import remote_player_wrapper
from ref_wrapper import Ref_Wrapper
from referee import Referee


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


config_data = get_config()
defaultFile = SourceFileLoader("default_player", config_data["default-player"]).load_module()

player1_wrap = remote_player_wrapper.RemotePlayerWrapper()
player2_wrap = defaultFile.default_player

try:
    player1_wrap.register()
except:
    player2_wrap.register()
    print(json.dumps([player2_wrap.get_name()]))
    sys.exit()

player2_wrap.register()

ref = Referee(player1_wrap, player2_wrap)
REF_WRAP = Ref_Wrapper(ref)
winner = REF_WRAP.play_game("remote", "default")

player1_wrap.close()
player1_wrap.sock.close()
print(json.dumps(winner, separators=(',', ':')))
