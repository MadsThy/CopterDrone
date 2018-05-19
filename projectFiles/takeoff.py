# Import DroneKit-Python
print "Wait 15 seconds for Dronekit to be imported"
from dronekit import connect, VehicleMode
from pymavlink import mavutil # Needed for command message definitions
from time import sleep
import math

# Connect to the Vehicle.
print "Connecting to drone"

# Connect to the Vehicle (in this case a simulator running the same computer)
vehicle = connect('udp:127.0.0.1:14550', wait_ready=['system_status','mode','armed'])
print "System status: %s" % vehicle.system_status.state
print "Mode: %s" % vehicle.mode.name    # settable
print "Armed: %s" % vehicle.armed    # settable
print "Heading: %s" % vehicle.heading
print "######################################"
print "#    Arming drone. Stand clear!!!    #"
print "######################################"

##########################################################################################

def turn(heading, relative, direction):
    print "Current Heading: %s" % vehicle.heading
        
    if relative:
        is_relative = 1 #yaw relative to direction of travel
        print "Turning", direction, heading, "degrees relative to current heading."
        if direction == "CW":
            newHeading = vehicle.heading+heading
            direction = 1
        else: 
            newHeading = vehicle.heading-heading
            direction = -1
        if newHeading>360:
            newHeading-360
        if newHeading<0:
            newHeading+360
        print "New Heading: %s" % newHeading
    else:
        is_relative = 0 #yaw is an absolute angle
        print "Turning to %s degrees absolute." % heading
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        direction,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
    while True:
        print "Current heading: %s" % vehicle.heading
        if direction == 1 and vehicle.heading>=newHeading:
            print "New heading reached"
            break
        elif direction == -1 and vehicle.heading<=newHeading:
            print "New heading reached"
            break
        sleep(0.5)

##########################################################################################

def arm_and_takeoff(aTargetAltitude):
    vehicle.mode    = VehicleMode("GUIDED")
    print " Waiting for arming..."
    sleep(13)
    vehicle.armed   = True

    sleep(2)
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        sleep(0.5)

##########################################################################################

arm_and_takeoff(vehicle.location.global_relative_frame.alt+1) # Fly up 1 meter relative to current altitude.

print("Take off complete - Hovering")

sleep(3)

turn(90,True,"CW")

sleep(3)

turn(90,True,"CCW")

print " Altitude before landing: ", vehicle.location.global_relative_frame.alt
sleep(3)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")
print " Altitude after landing: ", vehicle.location.global_relative_frame.alt
# Close vehicle object
vehicle.mode = VehicleMode("STABILIZE")

vehicle.armed  = False

vehicle.close()