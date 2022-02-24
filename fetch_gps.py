import os
import sys
import time
import smbus
import subprocess

from datetime import datetime

from gps import *

# Delay start by 15 seconds
time.sleep(15)

#os.system("sudo echo 1 > /sys/class/gpio/gpio9/value &")

# Write Headers to the log file
file = open('/home/pi/GPSLog.csv', 'a')
file.write("\n\n\n" + "CurrTimestamp" + "," + "GPSLat" + "," + "GPSLong" + "," + "GPSTime" + "," + "GPSAlt" + "," + "GPSStatus" + "\n")
file.close

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

x = 0

while 1:
#    print (x)

    GPSLat = "0.0"
    GPSLong = "0.0"
    GPSTime = "00:00:00"
    GPSAlt = "000"
    GPSMode = "0"
    GPSSats = "0"

# Get timestamp
    CurrTimestamp = datetime.now()
    report = gpsd.next()

    if report['class'] == 'TPV':
        GPSLat = getattr(report,'lat',0.0)
        GPSLong = getattr(report,'lon',0.0)
        GPSTime = getattr(report,'time','')
        GPSAlt = getattr(report,'alt','nan')
        GPSMode = getattr(report,'mode','nan')
        GPSSats = getattr(report,'sats','no sats')
    
    if GPSLat != "0.0" and GPSLong != "0.0" and GPSAlt != "nan":
        break
    x += 1

    if x == 30:
       break


with open('GPSFix.py', "w") as f:
#        f.write(f"timestamp = {CurrTimestamp}\n")
        f.write(f"lat = {GPSLat}\n")
        f.write(f"long = {GPSLong}\n")
#        f.write(f"gps_time = {GPSTime}\n")
        f.write(f"altitude = {GPSAlt}\n")
        f.write(f"mode = {GPSMode}\n")

# Write data to a log
file = open('GPSLog.csv', 'w')
file.write(str(CurrTimestamp) + "," + str(GPSLat) + "," + str(GPSLong) + "," + str(GPSTime) + "," + str(GPSAlt) +  "\n")
file.close
