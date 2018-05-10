#To be able to use the python script, dronekit must be installed. Dronekit can be installed by typing "pip install dronekit" in the terminal
import sys

#sys.argv is the parameter from node.js. This parameter is the input on the HTML page, i.e. the command which is sent to the Drone
print("Output from python: " + sys.argv[1])

#Connect to the Drone with an IP-adress and a port
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

#This is the method which takes the command from the HTML page. The command is then taken through some if else statements to check if the command is supported.
def arm_and_takeoff(aTargetAltitude){
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    #If command is fly up
    if(sys.argv[1] == "flyup"){
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
        vehicle.simple_takeoff(10) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
        #after Vehicle.simple_takeoff will execute immediately).
        while True:
            print " Altitude: ", vehicle.location.global_relative_frame.alt
            #Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt>=10*0.95:
                print "Reached target altitude"
                break
            time.sleep(1)

        arm_and_takeoff(10)
    } else if (sys.argv[1] == "flyup"){
        #TODO more commands
    }
}