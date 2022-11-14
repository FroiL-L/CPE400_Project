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