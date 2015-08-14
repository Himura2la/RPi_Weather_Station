import socket
import sys
import time
from subprocess import Popen

from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor
import Adafruit_DHT

DEVICE_MAC = 'b8-27-eb-1f-79-88'

bmp = BMP085.BMP085(0x77, 3)
lux = TSL2561.TSL2561()
dht = Adafruit_DHT.DHT22

weather = {}
for sensor in W1ThermSensor.get_available_sensors():
    weather[sensor.id] = sensor.get_temperature()

weather['T0'] = min(weather.values())
weather['T1'] = bmp.readTemperature()
weather['P1'] = bmp.readPressure() / 100.0
weather['L1'] = lux.getAnyLux()
weather['H1'], weather['T2'] = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)

Popen(['python','/home/pi/w/7seg.py', str(int(round(weather['T0'])))])

sock = socket.socket()
sock.connect(('narodmon.ru', 8283))

req = "#" + DEVICE_MAC + "\n"
for id in weather.keys():
    req += "#{}#{}\n".format(id, weather[id])
req += "##"

sock.send(req)

data = sock.recv(1024)
sock.close()
