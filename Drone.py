###########################################
# Drone.py:
#   Contains the Drone class definition
#   to create drones that act as relay
#   points in a network.
# @authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
###########################################

# Libraries
import Coords
import socket
import DroneUtils

from typing import Type

###########################################
# Drone:
#   Class for creating drones that act as
#   relay points in a network.
###########################################
class Drone:
    #radius that drones can reach is 1 km
    radius = 1000;
    def __init__(self, name: str,
                 port: int,
                 host: str,
                 coords: Type[Coords.Coords] = Coords.Coords()) -> None:
        self.name = name
        self.port = port
        self.coords = coords
        self.host = host
        self.gNFxn = DroneUtils.localSimGetNeighbors
        self.neighbors = []
        self.distances = []
    
    ###########################################
    # startUp():
    #   Initiates the drone to begin listening
    #   for incoming  messages.
    # args:
    #   NA.
    # return:
    #   NA.
    ###########################################
    def startUp(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    conn.sendall(bytes(1))
                    
    ###########################################
    # getNeighbors():
    #   Generate a list of neighbors within
    #   range of the current drone.
    # args:
    #   @N: List of neighbors to get neighbors
    #       from.
    # return:
    #   NA.
    ###########################################
    def getNeighbors(self, N: list):
        self.neighbors, self.distances = self.gNFxn(N, self, self.connection_radius)
        return self.neighbors, self.distances
        
    ###########################################
    # setGetNeighborsFxn():
    #   Set the function used to obtain the
    #   neighbors of the drone.
    # args:
    #   @fxn: Function to use.
    # return:
    #   NA.
    ###########################################
    def setGetNeighborsFxn(self, fxn):
        self.gNFxn = fxn
    
    def updateCoords(self, coords):
        self.coords = coords

    def getRadius(self):
        return Drone.radius

    def getCoords(self):
        return self.coords