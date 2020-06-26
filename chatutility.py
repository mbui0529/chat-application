"""
-----------------------------------------------------------------
socket.setblocking(0) -> # equivalent to s.settimeout(0.0)
if a recv() call doesn’t find any data, or if a send() call can’t
immediately dispose of the data, an error exception is raised.
-> Helps handle the error and keep data flowing.
-----------------------------------------------------------------
"""

import socket
import sys

MAX_USERS = 30
PORT = 55000
QUIT_STRING = '#exit'



def create_listen_socket(address):
    """
    create a listen socket when the server boosts up
    :param address: tuple
    :return: socket object
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow reuse the address
    s.setblocking(0)  # non-blocking, work with TCP
    s.bind(address)  # must bind the address before listen
    s.listen(MAX_USERS)  # listen up to MAX_USERS
    print("Now listening at ", address)
    return s


def welcome_prompt(new_user):
    """
    welcome prompt for a new user
    :param new_user: object
    :return:
    """
    new_user.socket.sendall(b'Welcome new user.\nPlease enter your name:\n')
    # use send all because of using TCP.


def remove_socket(socket, socket_list):
    """
    remove error socket from the socket list
    :param socket: object
    :param socket_list:  list of socket objects
    :return:
    """
    socket.close()  # close the socket
    return socket_list.remove(socket)  # return the socket from the list


