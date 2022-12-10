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
def localSimSendMessage(port: int,
                        ip: str,
                        message: bytes):
    currDir = os.getcwd()
    sp.Popen(["python3", "SimStartupDrone.py", ip, str(port)]) # Run executable that starts a drone
                                                                    # to begin listening for messages.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(message)
            
###########################################
# dijskra():
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
def genDijskraVector(G: list,
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