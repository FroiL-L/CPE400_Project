###########################################
# SimStartupDrone.py
#   Simulation tool used to execute one
#   drone at a time to listen for calls.
# usage:
#   $ python SimStartupDrone.py <host> <port>
#   @host: Host address to assign to drone.
#   @port: Port number to listen on.
# authors:
#   Froilan Luna-Lopez
#       University of Nevada, Reno
#       12 November 2022
###########################################

import sys
import Drone
import Coords

if len(sys.argv) != 7:
    print("Error: Incorrect number of arguments.")
    print("Usage: $ python SimStartupDrone.py <host> <port> <name> <x> <y> <z>")

HOST = sys.argv[1]
PORT = sys.argv[2]
name = sys.argv[3]
x    = sys.argv[4]
y    = sys.argv[5]
z    = sys.argv[6]

drone = Drone.Drone(name, int(PORT), HOST, Coords.Coords(x,y,z))
drone.startUp()
