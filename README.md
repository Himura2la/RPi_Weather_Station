# Raspberry Pi Weather Station
The online weather station based on Raspberry Pi

## Version 1.0
Was working for about three months. It has had only one sensor BMP085 which were collecting pressure and temperature to the MySQL database. 
The back-end was implementen in Python, the front-end -- in [DevExpress JS controls](http://js.devexpress.com/).

##Version 2.0
Is currently under development.
It includes three sensors.
* DS18B20 - to control temperature outside
* BMP085 - to control atmospheric pressure and temperature once again (it can be put to another place)
* TSL2561 - to control the lightness. Nobody measures the lightness! I'll be the first! Why not?

The library for TSL2561 was written from scratch based on the [official Adafruit library](https://github.com/adafruit/TSL2561-Arduino-Library) and the [official datasheet](http://www.adafruit.com/datasheets/TSL2561.pdf). Not all features are implemented (consider pull request?), but at least it gives the correct measurements in lux with the clear code for Python 2 (not just like [this](https://github.com/seanbechhofer/raspberrypi/blob/master/python/TSL2561.py) or [this](https://github.com/janheise/TSL2561))

