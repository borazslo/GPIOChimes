import sys, re
import mChimes as chimes

def error( message ):
    print "Error:",message
    sys.exit()

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == "-h":
        print "Example: set power=1"
        sys.exit()
    #SET command
    elif command == "set":
        if not len(sys.argv) > 2:
            error("What do you want to set?")        
        matchObj = re.search("^(.*?)=(.*?)$", sys.argv[2])
        if not matchObj:
            error("Invalid format")
        texttosend = matchObj.group() 
    elif command == "list":
        texttosend = "list"
    else:
        error("Invalid command")

    chimes.send (texttosend)  

else:
    print "Arguments needed"