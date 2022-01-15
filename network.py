'''
network.py
Description :
    Responsible for client's connection and communication to the server
'''

import socket
import pickle

'''
Network
Description :
    This class contains information and methods for client 
    to communicate with the server.
Initial parameters :
    client - client's socket object for socket connection
    server - the host server IP address
    port - the host server port (default as 5555)
    address - set of the server and port
    player - player ID (0 - white, 1 - red, or 2 - black)
Class parameters :
    self - the class's initial paramaters
    ip - the host IP address 
'''
class Network:
    def __init__(self, ip):
        socket.setdefaulttimeout(6)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip 
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()

    #Return the client's player ID (white, red, or black)
    def getPlayerID(self):
        return self.player

    #Connect the client to the server
    #Return received data
    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(262144).decode()
        except:
            pass

    #Send data to the server
    #Return received data 
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(262144*2))
        except socket.error as error:
            raise error