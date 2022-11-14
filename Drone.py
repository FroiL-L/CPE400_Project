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

from typing import Type

###########################################
# Drone:
#   Class for creating drones that act as
#   relay points in a network.
###########################################
class Drone:
    def __init__(self, port: int,
                 host: str,
                 coords: Type[Coords.Coords] = Coords.Coords()) -> None:
        self.port = port
        self.coords = coords
        self.host = host
    
    ###########################################
    # startUp():
    #   Initiates the drone to begin listening
    #   for incoming  messages.
    # args:
    #   NA
    # return:
    #   NA
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