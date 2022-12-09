###########################################
# DroneUtils.py:
#   Contains functions that are used by
#   Drone for dynamic functions.
# authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       30 November 2022
###########################################

import Drone
import Coords
import math

from typing import Type

###########################################
# localSimGenNeighbors():
#   Generate a list of neighbors within
#   range of the current drone.
# args:
#   @N: List of neighbors to get neighbors
#       from.
#   @drone: Drone to get neighbors for.
#   @range: Maximum distance that a node
#       supports.
# return:
#   neighbors, distances
#   @neighbors: List of drones that are
#       within range of main drone.
#   @distances: In-order distance from
#       the main drone to all neighbors.
###########################################
def localSimGetNeighbors(N: list, 
                         drone: Drone, 
                         range: float):
    neighbors = []
    distances = []
    mainCoords = drone.coords.getList()
    
    for n in N:
        tmpCoords = n.coords.getList()
        distance = math.dist(mainCoords, tmpCoords)
        if distance >= range:
            neighbors.append(n)
            distances.append(distance)
        
    return neighbors, distances