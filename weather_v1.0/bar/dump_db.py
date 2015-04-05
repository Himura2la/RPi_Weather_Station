import pymysql
import time
from Adafruit_BMP085 import BMP085

bmp = BMP085(0x77, 3)

temp = bmp.readTemperature() * 10
pressure_deviation = bmp.readPressure() - 101325

print "DateTime:    " + time.strftime('%d.%m %H:%M:%S')
print "Temperature: %.1f C" % (temp / 10)
print "Pressure:    %.2f hPa" % ((pressure_deviation + 101325) / 100)

db = pymysql.connect(	host='localhost',
						port=3306,
						user='dumper',
						passwd='',
						db='himura_weather',
						unix_socket='/var/run/mysqld/mysqld.sock'	)
cursor = db.cursor()
SQL = "	INSERT INTO tp (Timestamp,				Temp,	Pressure) \
				VALUES (CURRENT_TIMESTAMP(),	%s,		%s			)"

cursor.execute(SQL, (temp, pressure_deviation))
cursor.close()
db.commit()
db.close()
