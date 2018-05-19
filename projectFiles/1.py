# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 1337              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(3)

# ---------------------- Full flight plan ------------------------

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

# ---------------------- ARM and takeoff script ------------------------

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
print 'Connected by', addr

while True:
    output = conn.recv(1024);

    if output.strip() == "disconnect":
        conn.close()
        sys.exit("Received disconnect message.  Shutting down.")
        conn.send("dack")
    elif output == "":
        print "Message received from client:"
        print output
        conn.send("ack")
    elif output == "":
        print "Message received from client:"
        print output
        conn.send("ack")
    elif output == "":
        print "Message received from client:"
        print output
        conn.send("ack")
    elif output == "":
        print "Message received from client:"
        print output
        conn.send("ack")
    elif output:
        print "Message received from client:"
        print output
        conn.send("ack")
    print "Done receiving command"
    conn, addr = s.accept()
conn.close()