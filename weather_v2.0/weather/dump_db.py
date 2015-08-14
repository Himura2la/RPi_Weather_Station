import time
import pymysql
from subprocess import Popen

from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor
import Adafruit_DHT

bmp = BMP085.BMP085(0x77, 3)
thermometer = W1ThermSensor()
lux = TSL2561.TSL2561()

temps = []#{}
for sensor in W1ThermSensor.get_available_sensors():
    #temps[sensor.id] = sensor.get_temperature()
    temps.append(sensor.get_temperature())

temp = min(temps)
bartemp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0
light = lux.getAnyLux()
humidity, humtemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)

#Popen(['python','/home/pi/w/7seg.py', str(int(round(temp)))])

with open("/var/mysql_discoverer_pwd", "r") as f: passwd = f.read()[0:-1]
db = pymysql.connect(   host='localhost',
                        port=3306,
                        user='discoverer',
                        passwd=passwd,
                        db='meteopi',
                        unix_socket='/var/run/mysqld/mysqld.sock'    )
cursor = db.cursor()

SQL = "    INSERT INTO tttphl (Timestamp, TempOut, TempIn, TempAtt, Pressure, Humidity, Lightness) \
                VALUES (CURRENT_TIMESTAMP(), %s, %s, %s, %s, %s, %s)"
cursor.execute(SQL, (temp, bartemp, humtemp, pressure, humidity, light))

cursor.close()
db.commit()
db.close()
