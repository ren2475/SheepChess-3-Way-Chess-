'''
server.py
Description :
    Responsible for establishing a server and communication
    between each user in-game
'''

import socket
from _thread import *
import pickle

from pygame.key import name
from ChessEngine import GameState, Move

'''
Define server, port, and address
'''
SERVER = socket.gethostbyname(socket.gethostname())
print("IP => " + SERVER)
PORT = 5555
ADDRESS = (SERVER, PORT)
games = {}      #game object
playerCount = 0 #total players in the server


'''
Create server socket object via IPv4 protocol, TCP/IP socket connection
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind(ADDRESS)
except socket.error as error:
    str(error)

server.listen(5)
print("[SERVER START] Waiting for a connection")

'''
threaded_client
Description : 
    This method allows each player in the game session
    to communicate with the server, to play chess.
    Deletes the game session if detects a disconnection.
Parameter :
   connection - a socket connection
   playerID   - player white, red, or black
   gameID     - game ID (0,1,2,...)
Does not return value
'''

def threaded_client(connection, playerID, gameID):
    global playerCount
    connection.send(str.encode(str(playerID)))

    while True:
        try:
            data = connection.recv(524288).decode()
            if data != "getGame":
                print("server data = " + data)
            #If the game room exists, focus on the room
            if gameID in games:
                game = games[gameID]


                #If no data is received
                if not data:
                    print("no data")
                    break
                elif data != "getGame":
                    #If data is player's username
                    if data[0:4] == "Name":
                        try:
                            print(game[2])
                            game[2].append(data[4:])

                            print(data[4:])
                        except:
                            print("Name Error")

                    else:
                        game.append(data)             
                    
                #Send data to all clients in the game room
                connection.sendall(pickle.dumps(game))

                        
            else:
                print("no game found")
                break
        except:
            print("exception error")
            break

    print("Lost connection")
    try:
        del games[gameID]
        print("Closing Game", gameID)
    except:
        pass
    playerCount -= 1
    connection.close()


'''
Server main
'''
while True:
    #Create new socket for a new client connection.
    connection, address = server.accept()
    print("Connected to:", address)

    playerCount += 1
    playerID = "0"      #White
    gameID = (playerCount - 1)//3
    #First player joins the room
    if playerCount % 3 == 1:
        games[gameID] = [gameID,1,[]]
        print("Creating a new game...")

    #Second player
    elif playerCount % 3 == 2:
        playerID = "1"  #Red
        games[gameID][1] += 1 
    #Third player
    else:
        games[gameID][1] += 1 
        playerID = "2"  #Black

    #Initialize threaded_client for a user
    start_new_thread(threaded_client, (connection, playerID, gameID))