import Network
import Drone
import Coords
import Client
import os

HOST = "127.0.0.1"
PORT = 8008
FNAME = "Coords.py"
DEST = "4000,3000"

def testSendFileMessage(fname, client):
    fPath = os.path.join(os.getcwd(), fname)
    client.sendFile(fPath)

def testDij(client):
    import NetworkUtils as netu
    global FNAME
    global DEST
    
    distances = netu.genDijskraPath(client.network.drones,client.cnxnName,DEST)
    return distances

def generate_client(network):
    global HOST
    global PORT
    
    userCoords = Coords.Coords(3000,3000)
    
    client = Client.Client(PORT,HOST,userCoords,network)
    client.updateCoords(userCoords)
    
    return client

def generate_network():
    global HOST
    global PORT
    
    network = Network.Network()
    
    network.addDrone(Drone.Drone("3000,3000",PORT,HOST,Coords.Coords(3000,3000)))
    network.addDrone(Drone.Drone("4000,3000",PORT,HOST,Coords.Coords(4000,3000)))
    network.addDrone(Drone.Drone("2000,3000",PORT,HOST,Coords.Coords(2000,3000)))
    network.addDrone(Drone.Drone("3000,4000",PORT,HOST,Coords.Coords(3000,4000)))
    network.addDrone(Drone.Drone("3000,2000",PORT,HOST,Coords.Coords(3000,2000)))
    
    return network

def main():
    global FNAME
    
    network = generate_network()
    client = generate_client(network)
    path = testDij(client)
    print(path)
    testSendFileMessage(FNAME, client)
    
    return

if __name__ == "__main__":
    main()