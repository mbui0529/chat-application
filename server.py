"""
This file implements all the functions of the server entity.
The Server MUST start first. Server keeps a list of rooms.
It is a message hub. Every message must be received and
distributed to room destination by Server. The data structure
of the list of rooms is the dictionary. Dictionary makes
the program avoid looking up the room id whenever we
need to access to a room entity.
"""
from room import Room
from chatutility import QUIT_STRING


UI = b'Instructions:\n' \
     + b'[#ls] to list all rooms\n' \
     + b'[#join room_ID] to join/switch to a room\n' \
     + b'[#mk room_ID] to create to a room\n' \
     + b'[#to room_ID msg] to send messages\n' \
     + b'[#myrooms] to list your rooms\n' \
     + b'[#users roomID] to list room users\n' \
     + b'[#leave room_ID] to send messages\n' \
     + b'[#exit] to exit\n' \
     + b'\n'


def split_room_id(msg):
    """This function take a msg and exact the second word as a room id"""
    if len(msg.split()) >= 2:  # error check
        return msg.split()[1]
    else:
        return ''


class Server:
    def __init__(self):
        self.rooms = {}  # {room_id} dict of room object

    def process_msg(self, user, msg):
        """This function handles the msg as command from clients and process it"""
        print(user.name + ": " + msg)
        if "username:" in msg:
            name = msg.split()[1]  # take the second part of the msg
            user.name = name
            user.socket.sendall(UI)  # send back the UI
            print(user.addr,":", user.name)

        elif "#join" in msg:
            room_id = split_room_id(msg)
            if room_id:
                self.join_rooms(user, room_id)
            else:
                user.socket.sendall(b'invalid room name!\n' + UI)

        elif "#mk" in msg:
            room_id = split_room_id(msg)
            if room_id:
                if not self.create_rooms(room_id):
                    user.socket.sendall(b'room name is taken')
                else:
                    self.enter_exist_rooms(user,room_id)
            else:
                user.socket.sendall(b'invalid room name!\n' + UI)

        elif "#leave" in msg:
            room_id = split_room_id(msg)
            if room_id:
                self.leave_rooms(user,room_id)
            else:
                user.socket.sendall(b'invalid room name!\n' + UI)

        elif "#to" in msg:
            if len(msg.split()) < 3:
                msg = b'Invalid sending syntax.\n' \
                    + b'[#to room_ID msg] to send messages.\n'
                user.socket.sendall(msg)
            else:
                room_id = split_room_id(msg)
                new_msg = msg.split(' ', 2)[2]
                if room_id:
                    self.send_messages(user, new_msg.encode(), room_id)
                else:
                    user.socket.sendall(b'invalid room name!\n' + UI)

        elif "#myrooms" in msg:
            if not user.list_user_rooms():
                msg = b'Your are not in any room.\n + [help] to get helped.\n'
                user.socket.sendall(msg)

        elif "#users" in msg:
            room_id = split_room_id(msg)
            if room_id:
                if room_id in self.rooms:
                    self.rooms[room_id].list_users(user)
                else:
                    msg = b'room does not exist.'
                    user.socket.sendall(msg)
            else:
                msg = b'Invalid room id'
                user.socket.sendall(msg)

        elif "#ls" in msg:
            self.list_rooms(user)

        elif "#help" in msg:
            user.socket.sendall(UI)

        elif QUIT_STRING in msg:
            user.socket.sendall(QUIT_STRING.encode())
            self.remove_user(user)

        elif '#crash' in msg:
            # the user socket is closed at client. Cannot be communicated.
            self.remove_user(user)

        else:
            msg = b'Invalid cmd\n[#help] to get helped.'
            user.socket.sendall(msg)

    def list_rooms(self, user):
        """
        this sends to the user the list of all room names
        :param user: object
        :return: null
        """
        if len(self.rooms) == 0: # no room created
            msg = 'No rooms. Create your own!\n' \
                  + '[#mk room_id] to create a room.\n' \
                  + '[#help] to get helped.\n'
            user.socket.sendall(msg.encode())
        else:
            msg = 'List of rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())

    def create_rooms(self, room_id):
        """
        Create a new room with new id
        :param room_id: string
        :return: boolean
        """
        if room_id not in self.rooms:  # new room:
            new_room = Room(room_id)
            self.rooms[room_id] = new_room
            return True
        else:  # room name is taken
            return False

    def send_messages(self, user, msg, room_id):
        """
        send a message from a user to all users in a room
        :param user: object
        :param msg: str
        :param room_id: str
        :return:
        """
        if room_id not in self.rooms:
            msg = b'Room does not exist'
            user.socket.sendall(msg)
        elif not user.is_in_room(room_id):
            msg = b'You are not in the room'
            user.socket.sendall(msg)
        else:
            # send the message
            self.rooms[room_id].broadcast(user, msg)

    def leave_rooms(self,user, room_id):
        """
        remove user from a room
        :param user: object
        :param room_id: str
        :return:
        """
        # check if room_id exist
        if room_id not in self.rooms:
            msg = b'Room does not exist'
            user.socket.sendall(msg)
        elif not user.is_in_room(room_id):
            msg = b'You are not in the room '
            user.socket.sendall(msg)
        else:
            user.leave_room(room_id)  # remove room from user
            self.rooms[room_id].remove_user(user)  # remove user from room
            msg = 'You have left room ' + room_id
            user.socket.sendall(msg.encode())

    def join_rooms(self, user, room_id):
        """
        put a user into a room
        :param user: object
        :param room_id: str
        :return:
        """
        if room_id not in self.rooms:
            user.socket.sendall(room_id.encode() + b' does not exist!\n[#ls] to list all rooms!\n[#mk] room_id to create rooms!\n')
        else:
            if user.is_in_room(room_id):
                user.socket.sendall(b'You are already in room: ' + room_id.encode())
            else:
                self.enter_exist_rooms(user,room_id)

    def enter_exist_rooms(self,user, room_id):
        """
        put a user into a valid room
        :param user: object
        :param room_id: string
        :return:
        """
        self.rooms[room_id].users.append(user)
        self.rooms[room_id].welcome_prompt(user)
        user.enter_room(room_id)

    def remove_user(self, user):
        """
        remove a user from the server when it leaves
        :param user: objects
        :return:
        """
        # remove user from rooms
        if bool(user.rooms):
            for room_id in user.rooms:
                self.rooms[room_id].remove_user(user)
        print("User: " + user.name + " has left\n")