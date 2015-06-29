import time
import pymysql
from subprocess import Popen

from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor
import Adafruit_DHT

import sys
sys.path.insert(1,'/root/sec')
import passwords

bmp = BMP085.BMP085(0x77, 3)
thermometer = W1ThermSensor()
lux = TSL2561.TSL2561()

bartemp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0
temp = thermometer.get_temperature()
light = lux.getAnyLux()
humidity, humtemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)

Popen(['python','/home/pi/weather/7seg.py', str(int(round(temp)))])

db = pymysql.connect(   host='localhost',
                        port=3306,
                        user='adventurer',
                        passwd=passwords.mysql,
                        db='weather2',
                        unix_socket='/var/run/mysqld/mysqld.sock'    )
cursor = db.cursor()

SQL = "    INSERT INTO tttphl (Timestamp, TempOut, TempIn, TempAtt, Pressure, Humidity, Lightness) \
                VALUES (CURRENT_TIMESTAMP(), %s, %s, %s, %s, %s, %s)"
cursor.execute(SQL, (temp, bartemp, humtemp, pressure, humidity, light))

cursor.close()
db.commit()
db.close()
