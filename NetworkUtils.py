###########################################
# NetworkUtils.py
#   Contains functions that Network may
#   use, but that aren't encapsulated
#   within it.
# @author:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
###########################################

import subprocess as sp
import os
import socket
import sys
import time
import Drone

###########################################
# localSimSendMessage():
#   Locally simulates sending a message
#   from a sender to a receiver.
# args:
#   @port: Port number to send info to.
#   @ip: IP address to send info to.
#   @message: Message to send.
###########################################
def localSimSendMessage(path,
                        message: bytes,
                        drones):
    currDir = os.getcwd()
    
    droneDict = {i.name:i for i in drones}
    dronePath = {i:droneDict[i] for i in path}

    for destDrone in dronePath.values():
        # Extract data from destination drone
        ip = destDrone.getHost()
        port = destDrone.getPort()
        name = destDrone.getName()
        coords = destDrone.getCoords().getList()
        x,y,z = [str(i) for i in coords]
        
        # Start up simulation drone to listen for messages.
        pyComm = sys.executable
        command = [pyComm, "SimStartupDrone.py", str(ip), str(port), str(name), x, y, z]
        sp.Popen(command)
        time.sleep(1)
        # Send message
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                cxnxMade = False
                timeouts = 0
                while not cxnxMade and timeouts < 15:
                        try:
                                s.connect((ip, port))
                                cxnxMade = True
                        except:
                                timeouts += 1
                                time.sleep(1)
                if not cxnxMade and timeouts == 15:
                        print("Error: Could not establish connection.")
                        return
                s.sendall(message)
                #s.recv(1024)
        time.sleep(1)
            
###########################################
# getDijskraPath():
#       Produce a path vector from a
#       startingn node to a destination
#       node.
# args:
#       @G: Graph of nodes and edges that
#               make up the network.
#       @origin: Name of node to start path
#               finding at.
#       @dest: Name of destination node.
# return:
#       Path.
###########################################
def genDijskraPath(G: list,
                     origin: str,
                     dest: str):
        queue = {i.name:i for i in G}
        distances = {i.name:10000 for i in G}
        previous = {i.name: None for i in G}
        
        distances[origin] = 0
        
        while queue:
                # Get node with shortest distance
                nodeKey = getNearestNodeKey(queue, distances)
                nearestNode = queue[nodeKey]
                nearestDist = distances[nodeKey]
                
                # Test for destination
                if nodeKey == dest:
                        break
                
                # Remove node from queue
                queue.pop(nodeKey)
                
                # Loop through all neighbors of shortest distance
                secondNeighbors = nearestNode.neighbors
                secondDistances = nearestNode.distances
                for n in range(0, len(secondNeighbors)):
                        # Get distance to all of its neighbors
                        secondNeighbor = secondNeighbors[n].name
                        cost = nearestDist + secondDistances[n]
                        if cost < distances[secondNeighbor]:
                                distances[secondNeighbor] = cost
                                previous[secondNeighbor] = nodeKey
                        
        # Backtrack from destination to get path
        path = []
        currPos = dest
        while previous[currPos]:
                path.insert(0, currPos)
                currPos = previous[currPos]
        path.insert(0,currPos)
                
        return path

###########################################
# genConsvPath():
#       Generates a path that maximizes
#       the weakest link between the
#       source and destination node.
# args:
#       @G: Graph of nodes and edges that
#               make up the network.
#       @origin: Name of node to start path
#               finding at.
#       @dest: Name of destination node.
# return:
#       Path.
###########################################
def genConsvPath(G: list,
                     origin: str,
                     dest: str):
        class node:
                def __init__(self, entry) -> None:
                        self.entry = entry
                        self.visited = False                
        # Convert graph into a dictionary
        G_dict = {i.name:i for i in G}
        
        # Generate first iteration of neighbors into a queue
        queue = [{i.name:node(i) for i in G_dict[origin].neighbors}]
        
        # Iterate through neighbors
        prevNodeKey = [origin]
        path = []
        wl = 10000
        currWl = 9999
        while queue:
                # Extract neighbor metadata
                neighborSet = queue[0]
                neighborKeys = list(neighborSet.keys())
                
                # Test for no neighbors
                if len(neighborKeys) == 0:
                        queue.pop(0)
                        prevNodeKey.pop(0)
                        continue
                                
                # Extract first nested neighbors
                neighbors = neighborSet[neighborKeys[0]].entry.neighbors
                
                # Update queue (remove touched node)
                queue[0].pop(neighborKeys[0])
                
                if neighbors[0].battery < wl:
                        currWl = neighbors[0].battery
                
                # Test if next neighbor is destination
                if neighborKeys[0] == dest:
                        if currWl < wl: # Choose path with greatest weakest link
                                path = prevNodeKey.copy()
                                path.reverse()
                                path.append(dest)
                                wl = currWl
                        elif currWl == wl and len(path) > len(prevNodeKey) + 1: # Flip paths if less hops found
                                path = prevNodeKey.copy()
                                path.reverse()
                                path.append(dest)
                        continue
                
                #if neighbors[0].battery < wl:
                #        currWl = neighbors[0].battery
                
                # Update variables to recurse into nested neighbors
                if neighbors:
                        #newQueue = {i.name:node(i) for i in neighbors}
                        newQueue = {}
                        for i in neighbors:
                                if i.name not in prevNodeKey:
                                        newQueue[i.name] = node(i)
                        queue.insert(0, newQueue)
                        prevNodeKey.insert(0, neighborKeys[0])
                        continue
                else:
                        prevNodeKey.pop(0)
                
                
        return path

###########################################
###########################################

def getNearestNodeKey(nodes: dict,
                      distances: dict):
        shortestKey = list(nodes)[0]
        
        for d in nodes:
                if distances.get(d) < distances.get(shortestKey):
                        shortestKey = d
                        
        return shortestKey
