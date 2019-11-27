from helpers import *
import socket
import json


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

    def reset_for_new_game(self):
        self.register_flag = False
        self.receive_flag = False

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_color(self):
        return self.color

    def receive_response(self):
        # receives data from client socket
        try:
            data = self.accept_socket.recv(recv_size)
            request = json.loads(data.decode())
        except (socket.error, socket.timeout):
            raise Exception("No data received")
        return request.strip('\"')

    def register(self):
        if self.register_flag:
            return GONE_CRAZY
        self.register_flag = True
        self.accept_socket.send(json.dumps(["register"]).encode())
        try:
            response = self.receive_response()
            return response
        except socket.error:
            return GONE_CRAZY

    def receive_stones(self, stone):
        if self.receive_flag or not self.register_flag:
            return GONE_CRAZY
        self.receive_flag = True
        self.color = stone
        self.accept_socket.send(json.dumps(["receive-stones", stone]).encode())

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            if len(boards) > 3:
                return GONE_CRAZY
            self.accept_socket.send(json.dumps(["make-a-move", boards]).encode())
            try:
                response = self.receive_response()
                return response
            except socket.error:
                return GONE_CRAZY
        return GONE_CRAZY

    def end_game(self):
        self.accept_socket.send(json.dumps(["end-game"]).encode())
        self.receive_response()
