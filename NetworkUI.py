###########################################
# NetworkUI.py:
#   Containes the user interface print code as well as input code
# @authors:
#   Tristan Bailey
#       University of Nevada, Reno
###########################################

from time import sleep
from NetworkController import NetworkController
from Coords import Coords
import os

class NetworkUI:
    def __init__(self) -> None:
        self.controller = NetworkController()

    def addDrone(self):
        print("**************")
        print("Adding New Drone to Network")
        print("**************")
        self.unitWarning()
        name = input("Enter Drone's Name/ID: ")
        x = input("Enter drone's X cordinate: ")
        y = input("Enter drone's Y cordinate: ")
        self.controller.addDrone(name, x, y)
        self.clearTerminal()

    def moveDrone(self):
        print("**************")
        print("Updating Drone Location")
        print("**************")
        self.unitWarning()
        name = input("Enter Drone's Name/ID: ")
        x = input("Enter Drone's new X cordinate: ")
        y = input("Enter Drone's new Y cordinate: ")
        self.controller.moveDrone(name, x, y)
        self.clearTerminal()
    
    def selectNetworkMode(self):
        print("**************")
        print("Network Mode")
        print("**************")
        #TODO


    def sendFile(self):
        print("**************")
        print("Sending File")
        print("**************")
        print("Please Enter File path from current running directory (loc of NetworkApp")
        print("\tor add file to this directory")
        fname = input("Enter file name/path: ")
        self.controller.sendFile(fname)
        sleep(5)
        input("Press Enter to Continue")
        self.clearTerminal()


    def placeClient(self):
        print("**************")
        print("Replacing Client in Map")
        print("**************")
        self.unitWarning()
        x = input("Enter client's X cordinate: ")
        y = input("Enter client's Y cordinate: ")
        self.controller.moveClient(x, y)
        self.clearTerminal()

    def addClient(self):
        print("**************")
        print("Adding Client to Network")
        print("**************")
        self.unitWarning()
        x = input("Enter client's X cordinate: ")
        y = input("Enter client's Y cordinate: ")
        self.controller.addClient(x, y)
        self.clearTerminal()

    def displayNetwork(self):
        x = ""
        while(x != "e"):
            print("**************")
            print("Drone Layout: ")
            print("**************")
            print("read as x increasing from right to left and y increasing bottom to top")
            drones, gateways, client = self.controller.getNetworkLayout()
            matrix = []
            for i in range(20):
                row = []
                for i in range(20):
                    row.append('0')
                matrix.append(row)
            for drone in drones:
                cords = drone.getList()
                matrix[int(cords[1]/1000)][int(cords[0]/1000)] = '1'
            for gateway in gateways:
                cords = gateway.getList()
                matrix[int(cords[1]/1000)][int(cords[0]/1000)] = 'G'
            if(client != None):
                clientCords = client.getList()
                matrix[int(clientCords[1]/1000)][int(clientCords[0]/1000)] = 'C'

            for i in reversed(range(len(matrix))):
                for ele in matrix[i]:
                    print(ele, end='')
                print()
            print("Search for drone Id/Name By Coordinates or enter e to exit")
            x = input("Enter X coordinate: ")

            if(x != "e"):
                y = input("Enter Y coordinate: ")
                name = self.controller.getDroneByCoords(x, y)
                print("Drone at (" +x +", "+y+"): "+name)
                input("Press Enter to Continue")
            self.clearTerminal()

    def addGateway(self):
        print("**************")
        print("Adding Gateway to Network")
        print("**************")
        self.unitWarning()
        name = input("Enter Gateway's Name/ID: ")
        x = input("Enter Gateway's X cordinate: ")
        y = input("Enter Gateway's Y cordinate: ")
        self.controller.addGateway(name, x, y)
        self.clearTerminal()
    def moveGateway(self):
        print("**************")
        print("Updating Gateway Location")
        print("**************")
        self.unitWarning()
        name = input("Enter Gateway's Name/ID: ")
        x = input("Enter Gateway's new X cordinate: ")
        y = input("Enter Gateway's new Y cordinate: ")
        self.controller.moveGateway(name, x, y)
        self.clearTerminal()
    
    def clearTerminal(self):
        #windows
        #os.system('cls')

        #linux
        os.system('clear')


    def mainMenu(self):
        exit = False
        while(not(exit)):
            print("**************")
            print("Main Progam Menu")
            print("**************")
            print("Enter the following operations to perform the specified action on the drone network")
            print("0: exit")
            print("1: Add Drone")
            print("2: Move Drone by Name")
            print("3: Add Client")
            print("4: Move Client")
            print("5: Add Gateway")
            print("6: Move Gateway")
            print("7: Send Specified File to Gateway")
            print("8: Display Network")
            option = input("Enter option in form of number: ")
            # Clearing the Screen
            self.clearTerminal()
            exit = self.switchMenu(option)

    def switchMenu(self, option):
        if(option == "1"):
            self.addDrone()
        elif(option == "2"):
            self.moveDrone()
        elif(option == "3"):
            self.addClient()
        elif(option == "4"):
            self.placeClient()
        elif(option == "5"):
            self.addGateway()
        elif(option == "6"):
            self.moveGateway()
        elif(option == "7"):
            self.sendFile()
        elif(option == "8"):
            self.displayNetwork()
        elif(option == "0"):
            return True
        else:
            print("Please enter valid option: an interger from 1-8")
        return False
    def unitWarning(self):
        print("Please enter cordinates in thousands of meters with no label: Ex 2000")