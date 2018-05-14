import sys
#To be able to use the python script, dronekit must be installed. Dronekit can be installed by typing "pip install dronekit" in the terminal
from dronekit import connect

#sys.argv is the parameter from node.js. This parameter is the input on the HTML page, i.e. the command which is sent to the Drone
print("Drone command output from python: " + sys.argv[1] + " " + sys.argv[2])

#Connect to the Drone with an IP-adress and a port
vehicle = connect('/dev/ttyAMA0',baud=57600, wait_ready=True)

#This is the method which takes the command from the HTML page. The command is then taken through some if else statements to check if the command is supported.
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    aTargetAltitude = sys.argv[2]
    
    #If command is fly up
    if(sys.argv[1] == "flyup"):
        print "Basic pre-arm checks"
        # Don't try to arm until autopilot is ready
        while not vehicle.is_armable:
            print " Waiting for vehicle to initialise..."
            time.sleep(1)

        print "Arming motors"
        # Copter should arm in GUIDED mode
        vehicle.mode    = VehicleMode("GUIDED")
        vehicle.armed   = True

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)

        print "Taking off!"
        vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #after Vehicle.simple_takeoff will execute immediately).
        while True:
            print " Altitude: ", vehicle.location.global_relative_frame.alt
            #Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
                print "Reached target altitude"
                break
            time.sleep(1)

        arm_and_takeoff(20)