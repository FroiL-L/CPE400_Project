###########################################
# DroneUtils.py:
#   Contains functions that are used by
#   Drone for dynamic functions.
# authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       30 November 2022
###########################################

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
def localSimGetNeighbors(N, 
                         drone):
    link_neighbors = []
    distances = []
    mainCoords = drone.getCoords().getList()
    maxdist = drone.getRadius()

    for n in N:
        tmpCoords = n.getCoords().getList()
        distance = math.dist(mainCoords, tmpCoords)
        #handle edge case where drone is getting distance to itself
        if distance <= drone.getRadius() and distance > 0:
            link_neighbors.append(n)
            distances.append(distance)
        
    return link_neighbors, distances