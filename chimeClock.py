import datetime
import sys, zmq 

speed = 0.8

#Mute it during night hours
now=datetime.datetime.now()
if ( ( now.hour > 22 ) and ( now.minute > 10 ) ) or ( now.hour < 9 ):
    sys.exit(0)

port = "5555"

firstQuarter =  [1,speed,2,speed,3,speed,4,speed * 2]
secondQuarter = [3,speed,1,speed,2,speed,4,speed * 2, 3,speed,2,speed,1,speed,3,speed * 2]
thirdQuarter =  [1,speed,3,speed,2,speed,4,speed * 2, 4,speed,2,speed,1,speed,3,speed * 2, 1,speed,2,speed,3,speed,4,speed * 2]
fourthQuarter = [3,speed,1,speed,2,speed,4,speed * 2, 3,speed,2,speed,1,speed,3,speed * 2, 1,speed,3,speed,2,speed,4,speed * 2, 4,speed,2,speed,1,speed,3,speed * 2]
Hour = [0,speed * 4]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)

def preparePattern( array ):
    pattern = ""
    for i in range(0, len(array), 2):
        pattern = pattern + str(array[i]) + ":" + str(array[i+1])
        if i < len(array) - 2 :
            pattern = pattern + "-"        
    return pattern

def sound( array ):
    pattern = preparePattern(array)
    socket.send (pattern)  

if now.minute == 15:
    sound(firstQuarter)    
elif now.minute == 30:
    sound(secondQuarter)
elif now.minute == 45:
    sound(thirdQuarter)    
elif now.minute == 0:
    if(now.hour > 12):
        hour = now.hour - 11
    elif(now.hour == 0 ):
        hour = 12
    else:
        hour = now.hour
    hours = fourthQuarter
    for x in xrange(1,hour):
        hours = hours+Hour        
        pass
    sound(hours)

