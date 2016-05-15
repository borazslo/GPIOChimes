import mChimes as chimes

settings = {
    "power": "max", #max, dimmed, silent
    "silentHours": [23,9], #from, to, 0-24
    "dimmedHours": [21,9] #from, to, 0-24
}

chimes.init(settings)
while True:    
    chimes.serverListen()
