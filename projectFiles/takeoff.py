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
print "#    Arming drone. Stand clear!!!    #"
print "######################################"


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print " Waiting for vehicle to initialise..."
    #    sleep(1)
    #
    #    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    print " Waiting for arming..."
    sleep(13)


    # Confirm vehicle armed before attempting to take off
    vehicle.armed   = True

    sleep(2)
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            vehicle.mode    = VehicleMode("STABILIZE")
            sleep(1)
            vehicle.armed   = False
            break
        sleep(0.5)

arm_and_takeoff(vehicle.location.global_relative_frame.alt+0.5)