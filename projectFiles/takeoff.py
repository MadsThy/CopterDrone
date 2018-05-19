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

def condition_yaw(heading, relative=False):
    """
    Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).
    This method sets an absolute heading by default, but you can set the `relative` parameter
    to `True` to set yaw relative to the current yaw heading.
    By default the yaw of the vehicle will follow the direction of travel. After setting 
    the yaw using this function there is no way to return to the default yaw "follow direction 
    of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)
    For more information see: 
    http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
    """
    if relative:
        is_relative = 1 #yaw relative to direction of travel
    else:
        is_relative = 0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

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
            #vehicle.mode    = VehicleMode("STABILIZE")
            #sleep(1)
            #vehicle.armed   = False
            break
        sleep(0.5)


arm_and_takeoff(vehicle.location.global_relative_frame.alt+1) # Fly up 1 meter relative to current altitude.

print("Take off complete - Hovering")

sleep(5)

print "Turning 90 degrees"
degreesToTurn = 90
newHeading = vehicle.heading+degreesToTurn
print "Current Heading: %s" % vehicle.heading
print "New Heading: %s" % newHeading
condition_yaw(degreesToTurn,relative=True)
while True:
    print " Heading: %s" % vehicle.heading
    if vehicle.heading>=newHeading:
        print "New heading reached"
        break
    sleep(0.5)


print " Heading: %s" % vehicle.heading

print " Altitude before landing: ", vehicle.location.global_relative_frame.alt
# Hover for 5 seconds
sleep(5)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")
print " Altitude after landing: ", vehicle.location.global_relative_frame.alt
# Close vehicle object
vehicle.mode = VehicleMode("STABILIZE")

vehicle.armed  = False

vehicle.close()