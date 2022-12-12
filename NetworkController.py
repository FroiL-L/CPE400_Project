from Network import Network
from Coords import Coords
from Drone import Drone
from Client import Client

HOST = "127.0.0.1"
PORT = 8008

class NetworkController:
    def __init__(self) -> None:
        self.droneNetwork = Network()
    
    #adds a drone to the network
    def addDrone(self, name, x, y):
        self.droneNetwork.addDrone(Drone(name,PORT,HOST,Coords(int(x), int(y))))
    #adds a gateway to the network
    def addGateway(self, name, x ,y):
        gatewayDrone = Drone(name,PORT,HOST,Coords(int(x), int(y)))
        gatewayDrone.setGateway(True)
        self.droneNetwork.addDrone(gatewayDrone)
    
    def moveGateway(self, name, x ,y):
        self.moveDrone(name, x, y)

    #creates a client
    def addClient(self,x,y):
        self.client = Client(PORT,HOST,Coords(int(x), int(y)),self.droneNetwork)
        self.client.updateCoords(Coords(int(x), int(y)))
    
    def sendFile(self):
        #TODO
        pass
    #moves the client if there is a client, o.w. creates a client
    def moveClient(self, x, y):
        try:
            self.client.updateCoords(Coords(int(x), int(y)))
        except:
            self.addClient(x, y)
    def moveDrone(self, name, x, y):
        try:
            self.droneNetwork.updateDroneLocation(name, Coords(int(x), int(y)))
        except:
            self.addDrone(name, Coords(int(x), int(y)))

    #method for simple testing only
    def getNetwork(self):
        return self.droneNetwork

    def getNetworkLayout(self):
        drones, gateways = self.droneNetwork.getAllDroneCoords()
        try:
            return drones, gateways, self.client.getCoords()
        except:
            return drones, gateways, None
    
    def getDroneByCoords(self, x, y):
        return self.droneNetwork.getDroneByCoords(Coords(int(x), int(y)))