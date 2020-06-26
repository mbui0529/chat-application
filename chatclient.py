import select, socket, sys
import chatutility

READ_BUFFER = 4096

if len(sys.argv) < 2:
    print("Usage: Python3 chatclient.py [hostname]", file = sys.stderr) # Handle Error
    sys.exit(1)
else:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create TCP socket
    server_socket.connect((sys.argv[1], chatutility.PORT)) # connect to server on IP and Port

def prompt():
    print('$', end=' ', flush = True)  # avoid unexpected i/o.


print("Server is connected\n")  # check if the client connects to server.


msg = ''  # initialize the msg with empty string

input = [server_socket,sys.stdin]  # socket from which expect to read,

output = []  # socket to which we expect to write

error = []  # socket to which we expect to get error socket

try:
    while True:
        read_sockets, write_sockets, error_sockets = select.select(input, output, error)
        """
        select is a system call of OS. It monitors the status of file descriptor of the i/o channel.
        """
        for s in read_sockets:
            if s is server_socket: # incoming message from server
                m = s.recv(READ_BUFFER) # receive the message from server
                if not m:
                    print("Server Problem!")
                    sys.exit(2)
                else:
                    if m == chatutility.QUIT_STRING.encode():
                        print('Bye\n')
                        sys.exit(0)
                    else:
                        print(m.decode())
                        if 'Welcome new user.' in m.decode(): # welcome prompt
                            msg = 'username: '  # use msg to signal the server for the new user.
                        else:
                            msg = ''  # flush the msg
                        prompt()
            else: # not a server socket, open use stdin
                m = msg + sys.stdin.readline() # take input from clients.
                server_socket.sendall(m.encode()) # make sure msg sent completely. It differs from socket.send

        for s in error_sockets: # handle the error
            socket_list = chatutility.remove_socket(s, socket_list)
except KeyboardInterrupt:
    # close the sockets
    msg = '#crash'
    server_socket.sendall(msg.encode())  # tell the server that the client has a problem.
    server_socket.close() # close socket.
    print ('Bye\n')
