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

if len(sys.argv) != 3:
    print("Error: Incorrect number of arguments.")
    print("Usage: $ python SimStartupDrone.py <host> <port>")

HOST = sys.argv[1]
PORT = sys.argv[2]

drone = Drone.Drone(int(PORT), HOST)
drone.startUp()