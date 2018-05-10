import sys
#To be able to use the python script, dronekit must be installed. Dronekit can be installed by typing "pip install dronekit" in the terminal
from dronekit import connect

#sys.argv is the parameter from node.js. This parameter is the input on the HTML page, i.e. the command which is sent to the Drone
print("Drone status")