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

PORT = 8008
HOST = "127.0.0.1"
fPath = "/mnt/c/Users/froil/OneDrive/Documents/UNR/Classwork/CPE 400 - Computer Networking/Project/Coords.py"

# Establish network
network = Network.Network()
coords1 = Coords.Coords(1,1,1)
coords2 = Coords.Coords(-1,-1,-1)
network.addDrone(Drone.Drone(PORT, HOST, coords1))
network.addDrone(Drone.Drone(PORT, HOST, coords2))

# Establish client
coords3 = Coords.Coords(0,0,0)
client = Client.Client(PORT, HOST, coords3, network)
client.updateCoords(coords3)
client.sendFile(fPath)
