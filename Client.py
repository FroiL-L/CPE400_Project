###########################################
# Client.py:
#   Contains the Client object definition
#   to connect and send messagers through
#   a network.
# @author:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
###########################################

# Libraries
import Coords
import Network

from typing import Type

###########################################
# Client:
#   Class for established a connection with
#   a network and sending messages.
###########################################
class Client:
    def __init__(self, port: int,
                 host: str,
                 coords: Type[Coords.Coords] = Coords.Coords(),
                 network: Type[Network.Network] = Network.Network()) -> None:
        self.port = port        # Port number to communicate from.
        self.host = host        # Host address to communicate from.
        self.coords = coords    # Client geographical coordinates.
        self.network = network  # Network to pass messages through.
        self.cnxn = None        # IP of node that we are connected to.
        self.cnxnName = None    # Name of node that we are connected to. 
        
    ###########################################
    # updateCoords:
    #   Updates the client's geographical
    #   coordinates and runs any necessary
    #   protocols.
    # args:
    #   @coords: XYZ coordinates of client.
    # return:
    #   NA
    ###########################################
    def updateCoords(self, coords: Coords):
        self.coords = coords
        newCnxn = self.network.connect(coords)
        # Establish new connection only when new one is found.
        if newCnxn != self.cnxn:
            self.cnxn = newCnxn.getHost()
            self.cnxnName = newCnxn.getName()
    
    ###########################################
    # sendFile():
    #   Sends a file saved on the local machine
    #   to the network.
    # args:
    #   @filePath: Absolute path of file on
    #       the local machine to send.
    # return:
    #   @0: Success.
    #   @1: Failure.
    ###########################################
    def sendFile(self, filePath: str):
        if not self.cnxn:
            print("Error: Could not send file. There is \
                no connection established.")
            return 1
        
        try:
            with open(filePath, "rb") as f:
                contents = f.read()
        except OSError as e:
            print(e.strerror)
            return 1
        
        # Add file header to message
        hDelim = "$"
        fName = filePath.split("/")[-1]
        header = bytes(hDelim + fName + hDelim, "utf-8")
        contents = header + contents
        
        #TODO: Determine destination by gateway
        dest = self.network.getGateway()
        
        if not dest:
            print("Error: No gateways allocated.")
            return None
        
        self.network.sendMessage(self.cnxnName, dest, contents)
    def getCoords(self):
        return self.coords