"""
Rooms are created by Server. It has a list of users who participate
in the same room. Room entities are created by the server application
and managed by Server entity. The rooms are responsible for sending
messages to users. This helps server distinct messages from different
rooms. The data structure of rooms is list/array. The room entity does
not access to user object often, so using list/array helps the program
save memory.
"""

class Room:
    def __init__(self, name):
        self.users = []  # a list of users' socket
        self.name = name  # room name

    def welcome_prompt(self, from_user):
        """
        welcome a new user to the room
        :param from_user:
        :return:
        """
        msg = self.name + " welcomes: " + from_user.name + '\n'
        msg = msg + '[#users room_id] to list all user in this room\n'
        for user in self.users:
            try:
                user.socket.sendall(msg.encode())
            except:
                user.socket.close()

    def broadcast(self, from_user, msg):
        """
        send a message to all users in the room
        :param from_user: object
        :param msg: encoded string
        :return:
        """
        pre = self.name + ', ' + from_user.name + ':'
        msg = pre.encode() + msg
        for user in self.users:
            try:
                user.socket.sendall(msg)
            except:
                user.socket.close()

    def list_users(self, user):
        """
        list all users in the room
        :param user: object
        :return:
        """
        msg = ''
        for u in self.users:
            msg += u.name + ', '
        user.socket.sendall(b'Users in '+ self.name.encode() + b': ' + msg.encode())

    def remove_user(self, user):
        """
        remove a user from the list
        :param user: removing object
        :return:
        """
        self.users.remove(user)
        leave_msg = user.name.encode() + b" has left the room\n"
        self.broadcast(user, leave_msg)