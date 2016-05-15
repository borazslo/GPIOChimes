import datetime, sys, zmq 
import mChimes as chimes

speed = 0.8

firstQuarter  =  "1:%(speed)s-2:%(speed)s-3:%(speed)s-4:%(doubleSpeed)s" % {"speed": speed, "doubleSpeed": speed * 2}
secondQuarter =  "3:%(speed)s-1:%(speed)s-2:%(speed)s-4:%(doubleSpeed)s-3:%(speed)s-2:%(speed)s-2:%(speed)s-3:%(doubleSpeed)s" % {"speed": speed, "doubleSpeed": speed * 2}
thirdQuarter  =  "1:%(speed)s-3:%(speed)s-2:%(speed)s-4:%(doubleSpeed)s-4:%(speed)s-2:%(speed)s-1:%(speed)s-3:%(doubleSpeed)s-1:%(speed)s-2:%(speed)s-3:%(speed)s-4:%(doubleSpeed)s" % {"speed": speed, "doubleSpeed": speed * 2}
fourthQuarter =  "3:%(speed)s-1:%(speed)s-2:%(speed)s-4:%(doubleSpeed)s-3:%(speed)s-2:%(speed)s-1:%(speed)s-3:%(doubleSpeed)s-1:%(speed)s-3:%(speed)s-2:%(speed)s-4:%(doubleSpeed)s-4:%(speed)s-2:%(speed)s-1:%(speed)s-3:%(doubleSpeed)s" % {"speed": speed, "doubleSpeed": speed * 2}
Hour = "0:%(speed)s"% {"speed": speed * 4}

now=datetime.datetime.now()
if now.minute == 15:
    chimes.sound(firstQuarter)    
elif now.minute == 30:
    chimes.sound(secondQuarter)
elif now.minute == 45:
    chimes.sound(thirdQuarter)    
elif now.minute == 0:
    if(now.hour > 12):
        hour = now.hour - 11
    elif(now.hour == 0 ):
        hour = 12
    else:
        hour = now.hour    
    chimes.sound(fourthQuarter+'-%s' % '-'.join(str(Hour) for x in xrange(1,hour)))