###########################################
# testClient.py:
#   Runs a test instance for the network
#   protocol as the client.
# authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
###########################################

import Client
import Network
import Coords
import Drone
import os

PORT = 8008
HOST = "127.0.0.1"
fPath = os.path.join(os.getcwd(),"TrainOnBridge.jpg")
# Establish network
network = Network.Network()
coords1 = Coords.Coords(1000,1000,1000)
coords2 = Coords.Coords(-1000,-1000,-1000)
gateway = Drone.Drone("1", PORT, HOST, coords1)
gateway.setGateway(True)
network.addDrone(gateway)
network.addDrone(Drone.Drone("2", PORT, HOST, coords2))

# Establish client
coords3 = Coords.Coords(0,0,0)
client = Client.Client(PORT, HOST, coords3, network)
client.updateCoords(coords3)
client.sendFile(fPath)
