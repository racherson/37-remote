from helpers import *
import socket
import json


def get_config():
    with open('go.config') as config_file:
        config_data = json.load(config_file)
    return config_data


class RemotePlayerWrapper:
    def __init__(self):
        self.config_data = get_config()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.config_data["IP"], self.config_data["port"]))
        # shadow states
        self.register_flag = False
        self.receive_flag = False

    def get_socket_response(self):
        full_data = ""
        while True:
            # reads each packet and adds to fullData
            data = self.sock.recv(1024)
            full_data += str(data)
            if data == "":
                break
        return full_data

    def register(self):
        self.register_flag = True
        self.sock.send(["register"])
        return self.get_socket_response()

    def receive_stones(self, stone):
        if self.receive_flag:
            self.receive_flag = True
            self.sock.send(["receive-stones", stone])
            return self.get_socket_response()
        return "GO has gone crazy!"

    def make_a_move(self, boards):
        if self.receive_flag and self.register_flag:
            self.sock.send(["make-a-move", boards])
            return self.get_socket_response()
        return "GO has gone crazy!"
