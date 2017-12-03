#!/usr/bin/env python

import os
import signal
import sys
import time
import urllib
import json
from papirus import PapirusTextPos
#from papirus import LM75B
import argparse
from time import sleep, strftime
from datetime import datetime

url1 = "http://esp1.kenkl.org/temp"  # living-room sensor
url2 = "http://ardu1.kenkl.org"  # outside/DC sensor 

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    exec(open('/etc/default/epd-fuse').read())
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

# Let's define the lines we're gonna use. False in text holds updates to the screen until WriteAll() is called
text = PapirusTextPos(False, rotation = 0)
text.AddText("", 0,0,20,Id="1")
text.AddText("", 0,20,20,Id="2")
text.AddText("", 0,40,20,Id="3")
text.AddText("", 0,60,20,Id="4")
text.AddText("", 0,80,20,Id="5")

def exit_gracefully(signum, frame):
    # let's restore the original signal handlers
    signal.signal(signal.SIGTERM, original_sigterm)
    signal.signal(signal.SIGINT, original_sigint)
    signal.signal(signal.SIGHUP, original_sighup)

    # clean up gracefully here. bail when done.
    #text.Clear()
    one = 'shutdown at'
    two = getdatetimestr()

    # And update the text
    text.UpdateText("1", one)
    text.UpdateText("2", two)
    text.UpdateText("3", "")
    text.UpdateText("4", "")
    text.UpdateText("5", "")

    # Trigger the display to update
    text.WriteAll()
    
    sleep(4)
    sys.exit(0)

    #just in case we do something during cleanup that means we *shouldn't" exit, we want our handler to stay intact.
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGHUP, exit_gracefully)

def getdatetimestr():
    datenow = datetime.now().strftime('%Y%m%d')
    timenow = datetime.now().strftime('%H:%M')
    datetimenow = datenow + ' @ ' + timenow
    return datetimenow

def refreshdisplay():
    # Read ESP1 temp
    wr = urllib.urlopen(url1)
    wd = wr.read()

    # JSON needs double-quotes. Just in case we've been given single-quotes...
    wd = wd.replace("'", '"')
    response = json.loads(wd)

    # ...and parse out what we're after. 
    temp1 = response['temp']

    #build the output
    one = 'ESP1: ' + str(temp1)
    five = getdatetimestr()

    # And update the display
    text.UpdateText("1", one)
    text.UpdateText("5", five)

    # Let's get things from Ardu1
    wr = urllib.urlopen(url2)
    wd = wr.read()
    wd = wd.replace("'", '"')
    response = json.loads(wd)

    # Get the data...
    temp2 = response['datacentre']
    temp3 = response['outside']

    #... and build THOSE lines
    two = 'DC: ' + str(temp2)
    three = 'Outside: ' + str(temp3)

    # Finally, write those lines
    text.UpdateText("2", two)
    text.UpdateText("3", three)

    ''' On second thought, let's not. The LM75B is reading really high (30.5+ in a room at 22), and the line screws up the display of datetime on line 5 for some reason...
    # Let's grab the on-board temp sensor and use it for line four...
    sensor = LM75B()
    tempC = '{c:.2f}'.format(c=sensor.getTempCFloat())

    four = ("LM75B: " + tempC)
    text.UpdateText("4", four)
    '''

    # Trigger the display to update
    text.WriteAll()    

def main():

    while True:
        refreshdisplay()
        time.sleep(60)

if __name__ == '__main__':
        #store original SIGs to trap, then redirect them. 
    original_sigterm = signal.getsignal(signal.SIGTERM)
    original_sigint = signal.getsignal(signal.SIGINT)
    original_sighup = signal.getsignal(signal.SIGHUP)
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGHUP, exit_gracefully)

    main()


