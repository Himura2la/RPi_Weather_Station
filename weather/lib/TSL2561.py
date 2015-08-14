#!/usr/bin/env python

from time import sleep
from math import pow
from Adafruit_I2C import Adafruit_I2C

class TSL2561:
    i2c = None
    debug = False
    
    gain = 0
    # If gain = 0, device is set to low gain (1X)
    # If gain = 1, device is set to high gain (16X)
    
    tInt = 2
    # If tInt = 0, integration will be 13.7ms
    # If tInt = 1, integration will be 101ms
    # If tInt = 2, integration will be 402ms

    TSL2561_ADDR_0 = 0x29 # address with '0' shorted on board
    TSL2561_ADDR   = 0x39 # default address
    TSL2561_ADDR_1 = 0x49 # address with '1' shorted on board

    # TSL2561 registers
    TSL2561_CMD           = 0x80
    TSL2561_CMD_CLEAR     = 0xC0
    TSL2561_REG_CONTROL   = 0x00
    TSL2561_REG_TIMING    = 0x01
    TSL2561_REG_THRESH_L  = 0x02
    TSL2561_REG_THRESH_H  = 0x04
    TSL2561_REG_INTCTL    = 0x06
    TSL2561_REG_ID        = 0x0A
    TSL2561_REG_DATA_0    = 0x0C
    TSL2561_REG_DATA_1    = 0x0E

    def __init__(self, address=TSL2561_ADDR,  debug=False):
        self.i2c = Adafruit_I2C(address)
        self.debug = debug
        id = self.sensorID()
        if (id > 0):
            if debug: print "Sensor ID: %#x" % id
        else:
            if debug: print "No sensor found =("

    def sensorID(self):
        return self.i2c.readU8(self.TSL2561_CMD | self.TSL2561_REG_ID)

    def configure(self, gain=0, tInt=2):
        if gain <= 1 and tInt >= 0: self.gain = gain
        else: 
            print "gain should be 0 or 1"
            exit()       
        if tInt <= 2 and tInt >= 0: self.tInt = tInt
        else: 
            print "tInt should be from 0 to 2"
            exit()
        self.on()
        reg = 0
        if self.gain: reg |= (1<<4)
        reg |= self.tInt
        self.i2c.write8(self.TSL2561_CMD | self.TSL2561_REG_TIMING, reg)
        actual_reg = self.i2c.readU8(self.TSL2561_CMD | self.TSL2561_REG_TIMING)
        if actual_reg == reg:
            if self.debug:
                print "Configured: gain=%d; tInt=%2.1fms" % (gain, self.tInt_ms())
            return True
        return False

    def tInt_ms(self):
        return float({ 0: 13.7, 1: 101, 2: 402 }[self.tInt])
    
    def wait(self):
        if self.debug: print("Waiting %dms..." % self.tInt_ms())
        sleep((self.tInt_ms()+10)/1000)
    
    def on(self):
        self.i2c.write8(self.TSL2561_CMD | self.TSL2561_REG_CONTROL, 0x03)
        if self.debug: print("Power ON")

    def off(self):
        self.i2c.write8(self.TSL2561_CMD | self.TSL2561_REG_CONTROL, 0x00)
        if self.debug: print("Power OFF")

    def getData(self):
        self.wait()
        CH0 = self.i2c.readU16(self.TSL2561_CMD | self.TSL2561_REG_DATA_0)  # Visible + IR
        CH1 = self.i2c.readU16(self.TSL2561_CMD | self.TSL2561_REG_DATA_1)  # Visible only
        if self.debug: print "Sensor returned: %#x %#x" % (CH0, CH1)
        return CH0, CH1

    def getLux(self, data):
        if data[0] == 0xFFFF: return "Staturation"
        if data[1] == 0xFFFF: return "IR Staturation"
        
        CH0 = float(data[0]) # Visible + IR
        CH1 = float(data[1]) # Visible only

        if CH0 == 0: return 0
        ratio = CH1 / CH0
        
        CH0 *= 402.0 / self.tInt_ms()
        CH1 *= 402.0 / self.tInt_ms()
        
        if self.gain == 0: # No mistake here
            CH1 *= 16; CH0 *= 16
            
        if ratio <= 0.52: return 0.0315*CH0 - 0.0593*CH0*(pow(ratio, 1.4))
        if ratio > 0.52 and ratio <= 0.65: return 0.0229*CH0 - 0.0291*CH1
        if ratio > 0.65 and ratio <= 0.8: return 0.0157*CH0 - 0.0180*CH1
        if ratio > 0.8 and ratio <= 1.3: return 0.00338*CH0 - 0.00260*CH1
        if ratio > 1.3: return 0

    def getAnyLux(self):
        self.configure(gain=1)
        light = self.getLux(self.getData())   # Try with gain

        if type(light) != type(float()):
            self.off()
            self.configure()
            light = self.getLux(self.getData())   # Try without gain
            
            if type(light) != type(float()):
                self.off()
                self.configure(tInt=1)
                light = self.getLux(self.getData())   # Try 101ms
                
                if type(light) != type(float()):
                    self.off()
                    self.configure(tInt=0)
                    light = self.getLux(self.getData())   # Try 14ms
                    
                    if type(light) != type(float()):    # Give up. Too much light
                        light = 65535
        self.off()
        return light

