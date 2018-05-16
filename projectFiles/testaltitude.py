# Import DroneKit-Python
from dronekit import connect, VehicleMode
from time import sleep

# Connect to the Vehicle.
print "Connecting to drone"

# Connect to the Vehicle (in this case a simulator running the same computer)
vehicle = connect('udp:127.0.0.1:14550', wait_ready=['system_status','mode','armed'])
print "System status: %s" % vehicle.system_status.state
print "Mode: %s" % vehicle.mode.name    # settable
print "Armed: %s" % vehicle.armed    # settable
print "######################################"
print "#           TESTING ALTITUDE         #"
print "######################################"

print "Current Altitude: ", vehicle.location.global_relative_frame.alt
#vehicle.mode    = VehicleMode("GUIDED")
sleep(5)
print "Current Altitude: ", vehicle.location.global_relative_frame.alt
sleep(5)
print "Current Altitude: ", vehicle.location.global_relative_frame.alt
sleep(5)
print "Current Altitude: ", vehicle.location.global_relative_frame.alt

targetaltitude = vehicle.location.global_relative_frame.alt+0.5
print "Target Altitude: ", targetaltitude
vehicle.armed   = True

while not vehicle.armed:
    print " Waiting for arming..."
    sleep(1)
    print "Taking off!"

while True:
    print "Altitude: ", vehicle.location.global_relative_frame.alt, " - ",vehicle.mode
    if vehicle.location.global_relative_frame.alt>=targetaltitude:
        print "Reached target altitude"
        break
        sleep(1)
    sleep(0.5)
#vehicle.mode    = VehicleMode("STABILIZE")
vehicle.armed   = False