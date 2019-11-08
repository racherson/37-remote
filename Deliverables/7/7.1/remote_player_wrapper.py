from helpers import *
import socket
import json
import pickle


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


class RemotePlayerWrapper:
    def __init__(self):
        self.config_data = get_config()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # shadow states
        self.register_flag = False
        self.receive_flag = False

    def get_socket_response(self):
        return pickle.loads(self.sock.recv(2048))

    def register(self):
        if self.register_flag:
            return "GO has gone crazy!"
        self.register_flag = True
        self.sock.connect((self.config_data["IP"], self.config_data["port"]))
        self.sock.send(pickle.dumps(["register"]))
        return self.get_socket_response()

    def receive_stones(self, stone):
        if self.receive_flag or not self.register_flag:
            return "GO has gone crazy!"
        self.receive_flag = True
        # self.sock.connect((self.config_data["IP"], self.config_data["port"]))
        self.sock.send(pickle.dumps(["receive-stones", stone]))
        response = self.get_socket_response()
        return response

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            # self.sock.connect((self.config_data["IP"], self.config_data["port"]))
            self.sock.send(pickle.dumps(["make-a-move", boards]))
            return self.get_socket_response()
        return "GO has gone crazy!"
