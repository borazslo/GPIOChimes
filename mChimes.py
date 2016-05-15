import sys, time, datetime, re
import zmq, RPi.GPIO as GPIO


#Global Static Constants
CHIMES_PORT = 5555
CHIMES_ROD2PIN = {0: 37, 1: 36, 2: 33, 3: 31, 4: 29} #!! setmode GPIO.BOARD
CHIMES_POWERVALUES = {'max': 0.07, 'dimmed': 0.05} #in sec


#Global (empty) variables 
chimesPower = float
chimesSettings = []
chimesServer = False

def init( settings ):
    initGPIOs( CHIMES_ROD2PIN )
    initServer( CHIMES_PORT )
    setSettings(settings)

def initGPIOs( GPIOlist ):
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setwarnings(False)
    for pin in GPIOlist:
        GPIO.setup(GPIOlist[pin], GPIO.OUT,initial=GPIO.LOW) 

def initServer( port ):
    global chimesServer
    context = zmq.Context()
    chimesServer = context.socket(zmq.REP)
    chimesServer.bind("tcp://*:%s" % port)

def getDefaultSetting():
    defaults = {
        "power": "max", #max, dimmed, silent
        "silentHours": [24,9], #from, to, 0-24
        "dimmedHours": [21,9] #from, to, 0-24
    }
    return defaults

def setSettings( settings ):
    global chimesSettings
    chimesSettings = getDefaultSetting()
    for setting in settings:
        chimesSettings[setting] = settings[setting]


def serverListen():
    global chimesServer
    #  Wait for next request from client
    message = chimesServer.recv()
    print "Received request: ", message,
    
    obj = re.search("^(.*?)=(.*?)$", message)
    #List Variables
    if message == "list":
        global chimesSettings
        chimesServer.send(str(chimesSettings))
        print " => Done"
    #Variable Settings Command    
    elif obj:
        chimesServer.send(setVariable(obj.group(1),obj.group(2)))
        print " => Done"
    #Sound Patter
    elif not validatePattern(message):
        print "=> Invalid pattern!!"
        chimesServer.send("Invalid pattern!")
    else:          
        hitPattern(message, calculatePower())
        print "=> Done."
        chimesServer.send("Done.")


def sound ( pattern ):
    send(pattern)

def send ( message ):    
    context = zmq.Context()
    print "Connecting to chime-server..."
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:%s" % CHIMES_PORT)
    print "Sending:", message
    socket.send (message)
    print "Received reply:", socket.recv()


def validatePattern( subject ):
    pattern = "^([0-4]{1}:\d{1}(\.\d{1,2}|)(-|$))+$"
    matchObj = re.match(pattern, subject)            
    if not matchObj:        
        return False
    else:
        return True

def hitPattern( pattern, power ):
    hit = map(str, pattern.split('-'))
    for i in range(0, len(hit)):
        if hit[i] != '':
            tmp = map(float, hit[i].split(':'))
            hitRod(tmp[0], power)
            time.sleep(tmp[1])

def hitRod( number, power ):    
    GPIO.output(CHIMES_ROD2PIN[number], GPIO.HIGH)
    time.sleep(power)
    GPIO.output(CHIMES_ROD2PIN[number], GPIO.LOW)


def calculatePower():
    global chimesSettings
    now = datetime.datetime.now()
    if chimesSettings["power"] == "silent":
        power = 0
    elif ifBetweenHours(chimesSettings["silentHours"],now.hour):
        power = 0
    elif chimesSettings["power"] == "dimmed":
        power = CHIMES_POWERVALUES['dimmed']
    elif ifBetweenHours(chimesSettings["dimmedHours"],now.hour):
        power = CHIMES_POWERVALUES['dimmed']
    else:
        power = CHIMES_POWERVALUES['max']
    return power

def setVariable(name,value):
    global chimesSettings
    if name in chimesSettings:
        if name == "power":
            if value in ["max","dimmed","silent"]:
                chimesSettings[name] = value
                return "OK"
            else:
                return "Invalid value for power."
        elif name == "silentHours":
            obj = re.search("^\[(\d+),(\d+)\]$",value)
            if obj:
                chimesSettings[name] = [int(obj.group(1)),int(obj.group(2))]
                return "OK"
            else:
                return "Invalid value for silentHours."
        elif name == "dimmedHours":
            obj = re.search("^\[(\d+),(\d+)\]$",value)
            if obj:
                chimesSettings[name] = [int(obj.group(1)),int(obj.group(2))]
                return "OK"
            else:
                return "Invalid value for dimmedHours."
        else:
            return "Sorry."
    else:
        return "Invalid variable to set"

def ifBetweenHours( hours, hour):
    if hours[0] <= hours[1]:
        if hours[0] <= hour and hours[1] < hour:
            return True
    elif hours[0] > hours[1]:
        if hours[0] <= hour or hours[1] > hour:
            return True
    return False
