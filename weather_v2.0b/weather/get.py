#!/usr/bin/python

import sys
import time
from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor

bmp = BMP085.BMP085(0x77, 3)
thermometer = W1ThermSensor()
lux = TSL2561.TSL2561(debug=True)

bartemp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0
altitude = bmp.readAltitude()

temp = thermometer.get_temperature()

light = None

lux.configure(gain=1)
light = lux.getLux(lux.getData())   # Try with gain

if type(light) != type(float()):
    lux.off()
    lux.configure()
    light = lux.getLux(lux.getData())   # Try without gain
    
    if type(light) != type(float()):
        lux.off()
        lux.configure(tInt=1)
        light = lux.getLux(lux.getData())   # Try 101ms
        
        if type(light) != type(float()):
            lux.off()
            lux.configure(tInt=0)
            light = lux.getLux(lux.getData())   # Try 14ms
            
            if type(light) != type(float()):    # Give up. Too much light
                light = 65535
lux.off()

#datetime = str(datetime.datetime.now()).split(".")[0]
timestamp = time.time()

print "Temperature: %.3f C" % temp
print "Barometer Temperature: %.1f C" % bartemp
print "Pressure: %.2f hPa" % pressure
if light != None:
    print "Lightness: %.2f Lux" % light
#print "Timestamp: " + str(timestamp)
