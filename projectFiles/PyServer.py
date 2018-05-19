from threading import Thread
import socket
print "Wait 15 seconds for Dronekit to be imported"
from dronekit import connect, VehicleMode
from pymavlink import mavutil # Needed for command message definitions
from time import sleep
import math

vehicle = connect('udp:127.0.0.1:14550', wait_ready=['system_status','mode','armed'])

VERBOSE = False
IP_PORT = 22000


def debug(text):
    if VERBOSE:
        print "Debug:---", text

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
        conn.close()
        
        print "Client disconnected. Waiting for next client..."
        isConnected = False
        debug("SocketHandler terminated")

    def executeCommand(self, cmd):
        debug("Calling executeCommand() with  cmd: " + cmd)
        
        if cmd[:-1] == "go":
            print "Button pressed"
            self.conn.sendall("Command received.")
        if cmd[:-1] == "arm":
            print "Arming..."
            vehicle.armed = True
            print "Disconnecting..."
        if cmd[:-1] == "disarm":
            print "Disarming drone."
            vehicle.armed = False
        if cmd[:-1] == "fly":
            print "Disarming drone."
            vehicle.armed = False
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
serverSocket.listen(10)

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