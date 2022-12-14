###########################################
# Drone.py:
#   Contains the Drone class definition
#   to create drones that act as relay
#   points in a network.
# @authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
# @coauthor:
#   Tristan Bailey
#        University of Nevada, Reno
###########################################

# Libraries
import Coords
import socket
import DroneUtils
import os
import time

from typing import Type

###########################################
# Drone:
#   Class for creating drones that act as
#   relay points in a network.
###########################################
class Drone:
    #radius that drones can reach is 1 km
    radius = 1000
    def __init__(self, name: str,
                 port: int,
                 host: str,
                 coords: Type[Coords.Coords] = Coords.Coords()) -> None:
        self.name = name
        self.port = port
        self.coords = coords
        self.host = host
        self.gateway = False
        self.gNFxn = DroneUtils.localSimGetNeighbors
        self.neighbors = []
        self.distances = []
        self.radius = 1000
        self.battery = 100
        
        os.makedirs(os.getcwd() + "/" + name, exist_ok=True)
    
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
        fName = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            cxnxMade = False
            timeouts = 0
            while not cxnxMade and timeouts < 15:
                try:
                    s.bind((self.host, self.port))
                    cxnxMade = True
                except:
                    timeouts += 1
                    time.sleep(1)
            if not cxnxMade and timeouts == 15:
                print("Could not establish server connection.")
                return
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    fName = self.saveFile(data, fName)
                    #conn.sendall(bytes(1))
                    
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
        self.neighbors, self.distances = self.gNFxn(N, self)
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
    
    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
    
    def getName(self):
        return self.name
    
    def getGateway(self):
        return self.gateway
    
    def setGateway(self, switch: bool):
        if switch:
            self.gateway = True
        else:
            self.gateway = False
            
    def saveFile(self, contents, fName=None):
        delim = bytes("$", "utf-8")
        data = contents
        
        s = None
        e = None
        if not fName:
            s = None
            m = None
            e = None
            for _ in range(2):
                s, m, e = data.partition(delim)
                data = e
        else:
            s = fName
            e = contents
           
        with open(self.name + "/" + s.decode(), "ab+") as f:
            f.write(e)
        return s
