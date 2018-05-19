from threading import Thread
import socket
print "Wait 15 seconds for Dronekit to be imported"
from dronekit import connect, VehicleMode
from pymavlink import mavutil # Needed for command message definitions
from time import sleep
import math

vehicle = connect('udp:127.0.0.1:14550')

VERBOSE = True
IP_PORT = 22000


def debug(text):
    if VERBOSE:
        print "Debug:---", text

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

# ---------------------- class SocketHandler ------------------------
class SocketHandler(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        global isConnected
        debug("SocketHandler started")
        while True:
            
            cmd = ""
            try:
                debug("Calling blocking conn.recv()")
                cmd = self.conn.recv(1024)
            except:
                debug("exception in conn.recv()") 
                # happens when connection is reset from the peer
                break
            debug("Received cmd: " + cmd + " len: " + str(len(cmd)))
            if len(cmd) == 0:
                break
            self.executeCommand(cmd)
            break
        conn.close()
        
        print "Client disconnected. Waiting for next client..."
        isConnected = False
        debug("SocketHandler terminated")

    def executeCommand(self, cmd):
        debug("Calling executeCommand() with  cmd: " + cmd)
        
        if cmd[:-1] == "arm":
            print "Arming..."
            vehicle.armed = True

        elif cmd[:-1] == "disarm":
            print "Disarming drone."
            vehicle.armed = False

        elif cmd[:-1] == "fly":
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
        else:
            print "Invalid command received"
            self.conn.sendall("Invalid command received.")

# ----------------- End of SocketHandler -----------------------

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# close port when process exits:
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
debug("Socket created")
HOSTNAME = "" # Symbolic name meaning all available interfaces
try:
    serverSocket.bind((HOSTNAME, IP_PORT))
except socket.error as msg:
    print "Bind failed", msg[0], msg[1]
    vehicle.close()
    sys.exit()
serverSocket.listen(5)

print "Waiting for a connecting client..."
isConnected = False
while True:
    debug("Calling blocking accept()...")
    conn, addr = serverSocket.accept()
    print "Connected with client at " + addr[0]
    isConnected = True
    socketHandler = SocketHandler(conn)
    # necessary to terminate it at program termination:
    socketHandler.setDaemon(True)  
    socketHandler.start()
    t = 0
    while isConnected:
        print "Server connected for", t, "seconds."
        sleep(10)
        t += 10

