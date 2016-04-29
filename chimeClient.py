import sys, zmq

port = "5555"

context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)

if len(sys.argv) > 1:
    pattern = sys.argv[1]
    print "Sending pattern: ", pattern
    socket.send (pattern)  
    message = socket.recv()
    print "Received reply: ", message