###########################################
# Network.py:
#   Contains the Network class definition
#   to create a network of access points.
# @authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
###########################################

# Libraries
import socket
import Drone
import Coords
import NetworkUtils as netu
import math

from typing import Type

###########################################
# Network:
#   Class for creating and accessing a 
#   network of drone access points.
###########################################
class Network:
    def __init__(self) -> None:
        self.drones = []
        self.gateways = []
        self.droneCoords = []
        self.cnxn: socket.socket = None
        self.smp = netu.localSimSendMessage
        
    ###########################################
    # addDrone():
    #   Adds a drone to the network.
    # args:
    #   @newDrone: New drone object TBA.
    # return:
    #   NA
    ###########################################
    def addDrone(self, newDrone: Type[Drone.Drone]):
        self.drones.append(newDrone)
        self.droneCoords.append(newDrone.coords)
        
        # Test for gateway drone
        if newDrone.getGateway():
            self.gateways.append(newDrone)
        
        # Add to potential neighbors
        for drone in self.drones:
            drone.getNeighbors(self.drones)
        
    ###########################################
    # connect():
    #   Establish a connection with the
    #   closest relay point in the network.
    # args:
    #   @coords: XYZ coordinates of client.
    # return:
    #   str: String with relay point IP
    #       address.
    #   1: Failure.
    ###########################################
    def connect(self, coords: Type[Coords.Coords]):
        if len(self.drones) == 0:
            print("Error: Could not connect to network. No messengers \
                  in network.")
            return 1
        
        # Connect to closest drone
        coordsList = coords.getList()
        minDist = math.dist(self.drones[0].getCoords().getList(), coordsList)
        closestDrone = self.drones[0]
        for drone in self.drones:
            tmp_dist = math.dist(drone.getCoords().getList(), coordsList)
            if tmp_dist < minDist:
                minDist = tmp_dist
                closestDrone = drone
                
        return closestDrone
    
    ###########################################
    # sendMessage():
    #   Sends a message from a sender to a
    #   receiver.
    # args:
    #   @port: Port number to send info to.
    #   @ip: IP address to send info to.
    #   @message: Message to send.
    # return:
    #   0: Success.
    #   1: Failure.
    ###########################################
    def sendMessage(self, source: str,
                    dest: str,
                    message: bytes):
        # Find destination drone
        destDrone = None
        sourceDrone = None
        for drone in self.drones:
            if drone.getName() == source:
                sourceDrone = True
            elif drone.getName() == dest:
                destDrone = True
                
        # Edge case
        if not destDrone or not sourceDrone:
            print("Error: Drone not found.")
            return 1
             
        # Send message 
        path = netu.genDijskraPath(self.drones, source, dest)
        self.smp(path, message, self.drones)
            
        return 0
    
    ###########################################
    # setSMP():
    #   Assigns a function to use when to send
    #   a message when calling sendMessage().
    # args:
    #   @fxn: Function to use.
    # return:
    #   NA.
    ###########################################
    def setSMP(self, fxn):
        self.smp = fxn
        
    def getGateway(self):
        if len(self.gateways) == 0:
            return None
        
        return self.gateways[0].getName()