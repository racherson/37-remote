from helpers import *
import socket
import json
# import pickle


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
        # self.receive_request()

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
            data = self.accept_socket.recv(4096)
            request = data.decode()
        except (socket.error, socket.timeout):
            raise Exception("No data received")
        return request

    def register(self):
        if self.register_flag:
            return GONE_CRAZY
        self.register_flag = True
        print("sending register request")
        self.accept_socket.send('["register"]')
        try:
            return self.receive_request()
        except Exception as e:
            print("remote player register exception:", e)
            return GONE_CRAZY

    def receive_stones(self, stone):
        if self.receive_flag or not self.register_flag:
            return GONE_CRAZY
        self.receive_flag = True
        self.color = stone
        print("sending receive stones request")
        self.accept_socket.send('["receive-stones",' + stone + ']')
        # try:
        #     return self.receive_request()
        # except:
        #     return GONE_CRAZY

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            if len(boards) > 3:
                return GONE_CRAZY
            print("sending make a move request")
            self.accept_socket.send('["make-a-move", ' + boards + ']')
            try:
                return self.receive_request()
            except:
                return GONE_CRAZY
        return GONE_CRAZY

    def end_game(self):
        self.accept_socket.send('["end-game"]')
        self.receive_request()
