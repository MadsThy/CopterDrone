# Import DroneKit-Python
from dronekit import connect, VehicleMode
from time import sleep

# Connect to the Vehicle.
print "Connecting to drone"
vehicle = connect('/dev/ttyAMA0',baud=57600, wait_ready=['system_status','mode'])

print "System status: %s" % vehicle.system_status.state
print "Mode: %s" % vehicle.mode.name    # settable
print "######################################"
print "#    Arming drone. Stand clear!!!    #"
print "######################################"
sleep(2)
vehicle.armed = True
sleep(1)
vehicle.armed = False

# Close vehicle object before exiting script
vehicle.close()

print("Connection completed")