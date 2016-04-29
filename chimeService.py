import sys, zmq
import RPi.GPIO as GPIO
import time, datetime, re

port = "5555"
GPIO.setmode(GPIO.BOARD)
chimeRod2Pin = {0: 37, 1: 36, 2: 33, 3: 31, 4: 29} 
powerValues = {'max': 0.07, 'dimmed': 0.05} #in sec

GPIO.setwarnings(False)
for pin in chimeRod2Pin:
    GPIO.setup(chimeRod2Pin[pin], GPIO.OUT,initial=GPIO.LOW) 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

power = float

settings = {
    "power": "max", #max, dimmed, silent
    "silentHours": [21,9], #from, to, 0-24
    "dimmedHours": [23,9] #from, to, 0-24
}

def ifBetweenHours( hours, hour):
    if hours[0] <= hours[1]:
        if hours[0] <= hour and hours[1] < hour:
            return True
    elif hours[0] > hours[1]:
        if hours[0] >= hour or hours[1] < hour:
            return True
    return False


def calculatePower():
    now = datetime.datetime.now()
    if settings["power"] == "silent":
        power = 0
    elif ifBetweenHours(settings["silentHours"],now.hour):
        power = 0
    elif settings["power"] == "dimmed":
        power = powerValues['dimmed']
    elif ifBetweenHours(settings["dimmedHours"],now.hour):
        power = powerValues['dimmed']
    else:
        power = powerValues['max']
    return power

def hitRod( number ):    
    GPIO.output(chimeRod2Pin[number], GPIO.HIGH)
    time.sleep(power)
    GPIO.output(chimeRod2Pin[number], GPIO.LOW)

def hitPattern( pattern ):
    hit = map(str, pattern.split('-'))
    for i in range(0, len(hit)):
        if hit[i] != '':
            tmp = map(float, hit[i].split(':'))
            hitRod(tmp[0])
            time.sleep(tmp[1])

def validatePattern( subject ):
    pattern = "^([0-4]{1}:\d{1}(\.\d{1,2}|)(-|$))+$"
    matchObj = re.match(pattern, subject)            
    if not matchObj:        
        return False
    else:
        return True


def setVariable(name,value):
    if name in settings:
        if name == "power":
            if value in ["max","dimmed","silent"]:
                settings[name] = value
                return "OK"
            else:
                return "Invalid value for power."
        elif name == "silentHours":
            obj = re.search("^\[(\d+),(\d+)\]$",value)
            if obj:
                settings[name] = [int(obj.group(1)),int(obj.group(2))]
                return "OK"
            else:
                return "Invalid value for silentHours."
        elif name == "dimmedHours":
            obj = re.search("^\[(\d+),(\d+)\]$",value)
            if obj:
                settings[name] = [int(obj.group(1)),int(obj.group(2))]
                return "OK"
            else:
                return "Invalid value for dimmedHours."
        else:
            return "Sorry."
    else:
        return "Invalid variable to set"

while True:
    #  Wait for next request from client
    message = socket.recv()
    print "Received request: ", message,
    
    obj = re.search("^(.*?)=(.*?)$", message)
    #List Variables
    if message == "list":
        socket.send(str(settings))
        print " => Done"
    #Variable Settings Command    
    elif obj:
        socket.send(setVariable(obj.group(1),obj.group(2)))
        print " => Done"
    #Sound Patter
    elif not validatePattern(message):
        print "=> Invalid pattern!!"
        socket.send("Invalid pattern!")
    else:        
        power = calculatePower()
        hitPattern(message)
        print "=> Done."
        socket.send("Done.")
