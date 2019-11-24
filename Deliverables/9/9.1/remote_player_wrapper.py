from helpers import *
import socket
import json
import pickle


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


class RemotePlayerWrapper:
    def __init__(self, accept_socket):
        # shadow states
        self.register_flag = False
        self.receive_flag = False
        self.name = "no name"
        self.color = None
        self.accept_socket = accept_socket
        _ = self.receive_request()

    def reset_for_new_game(self):
        self.register_flag = False
        self.receive_flag = False

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_color(self):
        return self.color

    def receive_request(self):
        # receives data from client socket
        try:
            data = self.accept_socket.recv(1024)
            request = pickle.loads(data)
        except (socket.error, socket.timeout):
            raise Exception("No data received")
        return request

    def register(self):
        if self.register_flag:
            return GONE_CRAZY
        self.register_flag = True
        self.accept_socket.send(pickle.dumps(["register"]))
        print("register receive request")
        return self.receive_request()

    def receive_stones(self, stone):
        if self.receive_flag or not self.register_flag:
            return GONE_CRAZY
        self.receive_flag = True
        self.color = stone
        self.accept_socket.send(pickle.dumps(["receive-stones", stone]))
        print("receive stones receive request")
        return self.receive_request()

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            if len(boards) > 3:
                return GONE_CRAZY
            self.accept_socket.send(pickle.dumps(["make-a-move", boards]))
            print("make a move receive request")
            return self.receive_request()
        return GONE_CRAZY

    def end_game(self):
        self.accept_socket.send(pickle.dumps(["end-game"]))
