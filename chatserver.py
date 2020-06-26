import select, sys
from user import User
from server import Server
import chatutility as ulti

READ_BUFFER = 4096
if len(sys.argv) < 2:
    print("Usage: Python3 chatclient.py [hostname]", file = sys.stderr) # Handle Error
    sys.exit(1)
else:
    host = sys.argv[1]
    listen_socket = ulti.create_listen_socket((host, ulti.PORT))  # goes to chat utility
    server = Server() # initialize the server
    socket_list = []
    socket_list.append(listen_socket)

try:
    while True:
        # pass the list of socket into select to monitor.
        read_users, write_users, socket_errors = select.select(socket_list, [], [])

        for user in read_users:
            if user is listen_socket:  # user is new because it connects to listen socket
                new_socket, addr = user.accept()  # waiting for user connection
                new_user = User(new_socket, addr)  # creating a new user
                socket_list.append(new_user)  # add the socket of the new user
                ulti.welcome_prompt(new_user)  # send welcome msg to new user

            else: # not a new user -> send the message
                #import pdb; pdb.set_trace()
                try:
                    msg = user.socket.recv(READ_BUFFER) # receive msg from clients
                except:
                    user.socket.close() # help handle the crash clients
                if msg:
                    server.process_msg(user, msg.decode().lower()) # process msg and send msg back
                else:  # user does not exist
                    # remove the user's socket from the list
                    user.socket.close()
                    socket_list.remove(user)

        for s in socket_errors: # handle the error
            socket_list = ulti.remove_socket(s, socket_list)

except KeyboardInterrupt:
    # close the sockets
    listen_socket.close()
    print('Bye\n')