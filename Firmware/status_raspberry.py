import RPi.GPIO as GPIO
import urllib2
import time
import os

host = "http://garoahc.appspot.com";
location_opened = "/rest/status/open";
location_closed = "/rest/status/close";
location_macs = "/rest/macs";
token = "/1234";

sensor_pin = 7
pinStatus = True
updateDelay = 600 #10 minutes delay
lastUpdate=0

#SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def update_status():
        global pinStatus
        global lastUpdate

        pinStatus = GPIO.input(sensor_pin)
        lastUpdate = time.time()

        status_url=host
        if(GPIO.input(sensor_pin)):
                #Open
                print "Opened"
                status_url+=location_opened
        else:
                #Closed
                print "Closed"
                status_url+=location_closed

        status_url+=token
        response = urllib2.urlopen(status_url)

def update_macs():
        #macs_command = "sudo nmap -sP 192.168.1.1-154 | egrep -o ..:..:..:..:..:.."
        macs_command = "sudo arp-scan --interface eth0 -l | egrep -o ..:..:..:..:..:.."

        cmd = os.popen(macs_command)
        macs_str= cmd.read()
        cmd.close()

        macs_str = macs_str.replace("\n",";")
        macs_str = macs_str[:-1]

        macs_url=host+location_macs+"/"+macs_str+token
        #response = urllib2.urlopen(macs_url)
        print macs_url


while True:
        #Status changed or last change was to long ago.
        if ( (pinStatus != GPIO.input(sensor_pin)) or ( (time.time()-lastUpdate) >= updateDelay ) ):
                print "Updating Status"
                update_status()
                update_macs()
        time.sleep(1)
