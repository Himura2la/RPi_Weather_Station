#!/usr/bin/python

import sys
import time
from Adafruit_BMP085 import BMP085

bmp = BMP085(0x77, 3)

temp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0
altitude = bmp.readAltitude()
#datetime = str(datetime.datetime.now()).split(".")[0]
timestamp = time.time()


print "Temperature: %.1f C" % temp
print "Pressure:    %.2f hPa" % pressure
#print "Timestamp:   " + str(timestamp)


#with open('/var/www/himura_weather.csv', 'a') as f:
# f.write('\n' + str(timestamp) + ',' + str(temp) + ',' + str(pressure))

