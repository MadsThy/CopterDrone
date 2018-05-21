# PYTHON CLIENT Program that sends instant commands to the Python server program
import socket,sys

HOST = "127.0.0.1"    # The remote host
PORT = 1337              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print "SEND '"+sys.argv[1]+"' to "+HOST+":"+str(PORT)

s.sendall(sys.argv[1])
data = s.recv(1024)
s.close()
print 'RESPONSE:', repr(data)