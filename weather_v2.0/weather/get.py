#!/usr/bin/python

import sys
import time
from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor
import Adafruit_DHT

bmp = BMP085.BMP085(0x77, 3)
thermometer = W1ThermSensor()
lux = TSL2561.TSL2561()
dht = Adafruit_DHT.DHT22

bartemp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0
light = lux.getAnyLux()
temp = thermometer.get_temperature()
humidity, humtemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)

print "Temperature: %.3f C" % temp
print "Barometer Temperature: %.1f C" % bartemp
print "Hygrometer Temperature: %.1f C" % humtemp
print "Pressure: %.2f hPa" % pressure
print "Humidity: %.2f %%" % humidity
print "Lightness: %.2f Lux" % light
#print "Timestamp: " + str(time.time())
