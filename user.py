"""
User are created in the server application. They are managed by Room entity.
The users’ identification is usernames, every user is REQUIRED to provide a username.
Users entities also have information about their sockets (addresses and socket
objects). The Users entity manages a list of the id of rooms that this user is in.
The list will be used to check if users have the ability to send messages in a room.
The Clients will communicate with Server using IP and Port numbers through User
entities. The data structure of the list of room id is dictionary because we need
to access to find the room id very often.
"""

class User:
    def __init__(self, socket, addr, name="new user"):
        self.socket = socket  # pass socket to class
        self.addr = addr  # user IP and port
        self.name = name  # user name
        self.rooms = {}   # dict of string used to keep track room IDs of users
        self.socket.setblocking(0)

    def fileno(self):  # used for select.select()
        return self.socket.fileno()

    def list_user_rooms(self):
        """
        list all rooms of the user
        :return:
        """
        if bool(self.rooms):
            msg = "Your room: "
            for room in self.rooms:
                msg += room
            self.socket.sendall(msg.encode())
            return True
        else:
            return False

    def enter_room(self,room_id):
        """
        add room id to the managing list
        :param room_id: str
        :return:
        """
        self.rooms[room_id] = room_id

    def leave_room(self, room_id):
        """
        remove room using room id from the managing list
        :param room_id: str
        :return:
        """
        self.rooms.pop(room_id)

    def is_in_room(self, room_id):
        """
        check if the user is in the room
        :param room_id: str
        :return:
        """
        if room_id in self.rooms:
            return True
        else:
            return False

