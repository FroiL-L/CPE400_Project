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

from typing import Type

###########################################
# Network:
#   Class for creating and accessing a 
#   network of drone access points.
###########################################
class Network:
    def __init__(self) -> None:
        from NetworkUtils import localSimSendMessage as lsmp
        self.drones = []
        self.droneCoords = []
        self.cnxn: socket.socket = None
        self.smp = lsmp
        
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
        # TODO: Choose drone based on distance
        return self.drones[0].host
    
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
    def sendMessage(self, port: int,
                    ip: str,
                    message: bytes):
        self.smp(port, ip, message)
            
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