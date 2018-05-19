import socket,sys

print "Script called with following arguments: " + sys.argv[1]

HOST = "127.0.0.1"    # The remote host
PORT = 1337              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print "Sending command '"+sys.argv[1]+"'"
s.sendall(sys.argv[1])
data = s.recv(1024)
s.close()
print 'Received', repr(data)