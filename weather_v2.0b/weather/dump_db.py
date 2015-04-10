import time
import pymysql
from lib import BMP085
from lib import TSL2561
from w1thermsensor import W1ThermSensor

bmp = BMP085.BMP085(0x77, 3)
thermometer = W1ThermSensor()
lux = TSL2561.TSL2561()#debug=True)

bartemp = bmp.readTemperature()
pressure = bmp.readPressure() / 100.0

temp = thermometer.get_temperature()


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


db = pymysql.connect(    host='localhost',
                        port=3306,
                        user='',
                        passwd='',
                        db='weather2',
                        unix_socket='/var/run/mysqld/mysqld.sock'    )
cursor = db.cursor()
SQL = "    INSERT INTO ttpl (Timestamp, TempOut, TempIn, Pressure, Lightness) \
                VALUES (CURRENT_TIMESTAMP(), %s, %s, %s, %s)"

cursor.execute(SQL, (temp, bartemp, pressure, light))
cursor.close()
db.commit()
db.close()
