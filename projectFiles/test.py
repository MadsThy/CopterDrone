# Import DroneKit-Python
from dronekit import connect, VehicleMode
from time import sleep

# Connect to the Vehicle.
print "Connecting to drone"
vehicle = connect('udp:127.0.0.1:14550')

print "System status: %s" % vehicle.system_status.state
print "Mode: %s" % vehicle.mode.name    # settable
print "######################################"
print "#    Arming drone. Stand clear!!!    #"
print "######################################"
sleep(2)
vehicle.armed = True
print "Disarming in..."
print "3..."
sleep(1)
print "2..."
sleep(1)
print "1..."
sleep(1)
vehicle.armed = False

# Close vehicle object before exiting script
vehicle.close()

print("Connection completed")