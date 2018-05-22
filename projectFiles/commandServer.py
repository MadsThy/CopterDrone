# PYTHON SERVER Program that receives instant commands from the client program
from threading import Thread
import socket,sys,math,logging,os
logging.basicConfig(level=logging.INFO)
from dronekit import connect, VehicleMode
logging.info("Dronekit imported.")
from pymavlink import mavutil # Needed for command message definitions
from time import sleep

HOST = ''               # Symbolic name meaning all available interfaces
PORT = 1337             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))    # Bind to host at port
s.listen(5)             #Accept 5 connections at any one time
logging.info("Server listening on localhost:"+str(PORT))

vehicle = connect('udp:127.0.0.1:14550',wait_ready=True)
print "Server ready."

# ---------------------- YAW-control SCRIPT ------------------------

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

# ---------------------- ARM and TAKEOFF script ------------------------

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

# ---------------------- Connection and arguments ------------------------

conn, addr = s.accept()
print 'Connection started by:', addr

while True:
    command = conn.recv(1024);

    if command.strip() == "disconnect":
        conn.send("Stop server - Bye")
        conn.close()
        vehicle.close()
        sys.exit("Received disconnect message.  Shutting down.")
        
    elif command == "mission":
        print "Message received from client:", command
        conn.send("OK - Mission")
        
        arm_and_takeoff(vehicle.location.global_relative_frame.alt+1) # Fly up 1 meter
        sleep(3)
        turn(180,True,"CW")
        sleep(3)
        turn(180,True,"CCW")
        sleep(3)
        vehicle.mode = VehicleMode("LAND")
        # Close vehicle object and disarm
        vehicle.mode = VehicleMode("STABILIZE")
        vehicle.armed  = False
    
    elif command == "panic":
        print "Message received from client:", command
        conn.send("OK - PANIC")
        
        vehicle.mode = VehicleMode("STABILIZE")
        vehicle.armed = False
        
    elif command == "arm":
        print "Message received from client:", command
        vehicle.armed = True
        conn.send("OK - Arm")
        
    elif command == "disarm":
        print "Message received from client:", command
        vehicle.armed = False
        conn.send("OK - Disarm")
    elif command == "reboot":
        print "Message received from client:", command
        os.system('sudo shutdown -r now')
        conn.send("OK - Shutting down")
        
    elif command == "":
        print "Message received from client:", command
        conn.send("ack")
        
    else:
        print "Received unrecognised command' "+command+"'"
        conn.send("Failure - Unrecognised command")
        
    conn, addr = s.accept() #restart command acceptance
conn.close()