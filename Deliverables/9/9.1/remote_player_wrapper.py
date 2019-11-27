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
        # self.receive_response()

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
            data = self.accept_socket.recv(4096)
            request = data.decode()
            print("received", request)
        except (socket.error, socket.timeout):
            print("couldn't receive anything!")
            raise Exception("No data received")
        return request

    def register(self):
        if self.register_flag:
            return GONE_CRAZY
        self.register_flag = True
        print("sending register request")
        self.accept_socket.send('["register"]'.encode())
        try:
            return self.receive_response()
        except Exception as e:
            print("remote player register exception:", e)
            return GONE_CRAZY

    def receive_stones(self, stone):
        if self.receive_flag or not self.register_flag:
            return GONE_CRAZY
        self.receive_flag = True
        self.color = stone
        print("sending receive stones request")
        message = '["receive-stones", ' + stone + ']'
        self.accept_socket.send(message.encode())
        # try:
        #     return self.receive_request()
        # except:
        #     return GONE_CRAZY

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            if len(boards) > 3:
                return GONE_CRAZY
            print("sending make a move request")
            to_send = '["make-a-move", ' + boards + ']'
            self.accept_socket.send(to_send.encode())
            try:
                response = self.receive_response()
                print("get back from make a move", response)
                return response
            except:
                print("can't get a move")
                return GONE_CRAZY
        return GONE_CRAZY

    def end_game(self):
        self.accept_socket.send('["end-game"]'.encode())
        self.receive_response()
