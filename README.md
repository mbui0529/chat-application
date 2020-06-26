# IRC - Internetworking Protocol Project
## Spring 2020
### Author: Matthew Bui

This specification describes a simple IRC protocol by which clients can communicate with each other. The server receives messages from clients and distributes them over the users that are in the same rooms.
 
Users can create rooms, which are groups of users that are subscribed to the same message stream. Besides, users can join and leave rooms. Joining rooms can be done simultaneously.
 
The utility functions are to list all user in a specific room, to list all rooms in the server, and to list all rooms that a user are being in.

To run the program:
* run ```python3 chatserver.py 127.0.0.1``` first.
* open a new terminal and run ```python3 chatclient.py 127.0.0.1```.
* open another terminal and re-run the client application.

When providing room id in the application, remember the room id is spitted by ' ' space char.

```#mk room1``` -> create a new room named room 1

`` #join room1`` -> join to room1

```#to room1 hey there``` -> send to room 1 a message "hey there"

```#leave room1``` -> leave room 1

...