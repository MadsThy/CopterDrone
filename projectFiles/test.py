# Import DroneKit-Python
from dronekit import connect, VehicleMode
from time import sleep

# Connect to the Vehicle.
print "Connecting to drone"
vehicle = connect('127.0.0.1:14550', wait_ready=['system_status','mode','armed'])

print "System status: %s" % vehicle.system_status.state
print "Mode: %s" % vehicle.mode.name    # settable
print "Armed: %s" % vehicle.armed    # settable
print "Is Armable?: %s" % vehicle.is_armable
print "CURRENT ALTITUDE: ", vehicle.location.global_relative_frame.alt
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
print " Altitude: ", vehicle.location.global_relative_frame.alt

# Close vehicle object before exiting script
vehicle.close()

print("Connection completed")