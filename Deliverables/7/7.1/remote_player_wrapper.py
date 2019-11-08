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
        # shadow states
        self.register_flag = False
        self.receive_flag = False
        # establish connection
        self.config_data = get_config()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.config_data["IP"], self.config_data["port"]))
        self.sock.listen(5)
        self.accept_socket, address = self.sock.accept()
        _ = self.receive_request()

    def receive_request(self):
        # receives data from client socket
        data = self.accept_socket.recv(1024)
        request = pickle.loads(data)
        return request

    def register(self):
        if self.register_flag:
            return "GO has gone crazy!"
        self.register_flag = True
        self.accept_socket.send(pickle.dumps(["register"]))
        return self.receive_request()

    def receive_stones(self, stone):
        if self.receive_flag or not self.register_flag:
            return "GO has gone crazy!"
        self.receive_flag = True
        self.accept_socket.send(pickle.dumps(["receive-stones", stone]))
        return self.receive_request()

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            self.accept_socket.send(pickle.dumps(["make-a-move", boards]))
            return self.receive_request()
        return "GO has gone crazy!"
