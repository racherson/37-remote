import json
from importlib.machinery import SourceFileLoader
import remote_player_wrapper
from ref_wrapper import Ref_Wrapper


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


config_data = get_config()
defaultFile = config_data["default-player"]
foo = SourceFileLoader("default_player", "default_player.py").load_module()
from foo.MyClass() import default_player


player1_wrap = remote_player_wrapper.RemotePlayerWrapper()
player2_wrap = default_player

player1_wrap.register()
player2_wrap.register()

REF_WRAP = Ref_Wrapper(player1_wrap, player2_wrap)
winner = REF_WRAP.play_game()

player1_wrap.close()
player1_wrap.sock.close()
print(json.dumps(winner, separators=(',', ':')))
