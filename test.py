import Network
import Drone
import Coords
import Client
import os

from NetworkController import NetworkController

HOST = "127.0.0.1"
PORT = 8008
FNAME = "Coords.py"
DEST = "4000,3000"

def testSendFileMessage(fname, client):
    fPath = os.path.join(os.getcwd(), fname)
    client.sendFile(fPath)
    
def testSaveFile(drone):
    global FNAME
    filePath = os.path.join(os.getcwd(), FNAME)
    try:
        with open(filePath, "rb") as f:
            contents = f.read()
    except OSError as e:
        print(e.strerror)
        return 1
    
    # Add file header to message
    hDelim = "$"
    fName = "Coords.py"
    header = bytes(hDelim + fName + hDelim, "utf-8")
    contents = header + contents
    
    drone.saveFile(contents)
    

def testDij(client):
    import NetworkUtils as netu
    global FNAME
    global DEST
    
    dest = client.network.getGateway()
    distances = netu.genDijskraPath(client.network.drones,client.cnxnName,dest)
    return distances

def testConsv(client):
    import NetworkUtils as netu
    global DEST
    
    dest = client.network.getGateway()
    distances = netu.genConsvPath(client.network.drones, client.cnxnName, dest)
    return distances

def generate_client(network):
    global HOST
    global PORT
    
    userCoords = Coords.Coords(3000,3000)
    
    client = Client.Client(PORT,HOST,userCoords,network)
    client.updateCoords(userCoords)
    
    return client

def generate_network(controller):
    print("Using controller")
    controller.addDrone("3000,3000",3000,3000)
    controller.addDrone("4000,3000",4000,3000)
    controller.addDrone("2000,3000",2000,3000)
    controller.addDrone("3000,4000",3000,4000)
    controller.addDrone("3000,2000",3000,2000)
    controller.addGateway("1000,3000", 1000,3000)
   
    return controller.getNetwork()

def main():
    global FNAME
    controller = NetworkController()
    network = generate_network(controller)
    network.setMode(1)
    client = generate_client(network)
    #path = testDij(client)
    path = testConsv(client)
    #print(path)
    testSendFileMessage(FNAME, client)
    
    return

if __name__ == "__main__":
    main()
