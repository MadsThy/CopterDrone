# PYTHON CLIENT Program that sends instant commands to the Python server program
import socket,sys

HOST = "127.0.0.1"    # The remote host
PORT = 1337              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # First we make a socket object
s.connect((HOST, PORT)) # Then we connect to the IP address with same port as the server uses. 
print "SEND '"+sys.argv[1]+"' to "+HOST+":"+str(PORT) # print string

s.sendall(sys.argv[1])
data = s.recv(1024) # Then we can recieve data from the server
s.close() # Now, closing the connection
print 'RESPONSE:', repr(data)