#!/usr/bin/python

import sys
import time
from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor
import Adafruit_DHT

bmp = BMP085.BMP085(0x77, 3)
lux = TSL2561.TSL2561()
dht = Adafruit_DHT.DHT22

temps = {}
for sensor in W1ThermSensor.get_available_sensors():
    temps[sensor.id] = sensor.get_temperature()

bartemp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0
light = lux.getAnyLux()
humidity, humtemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)


for id in temps.keys():
    print "Temperature on %s: %.3f C" % (id, temps[id])

print "Barometer Temperature: %.1f C" % bartemp
print "Hygrometer Temperature: %.1f C" % humtemp
print "Pressure: %.2f hPa" % pressure
print "Humidity: %.2f %%" % humidity
print "Lightness: %.2f Lux" % light
#print "Timestamp: " + str(time.time())
