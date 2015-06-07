import RPi.GPIO as GPIO
import sys
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SR_DATA = 17;
SR_SHIFT = 4;
SR_LOCK = 27;

GPIO.setup(SR_DATA, GPIO.OUT)
GPIO.setup(SR_SHIFT, GPIO.OUT)
GPIO.setup(SR_LOCK, GPIO.OUT)


def SR_Write(n):
    for i in range(0,8):
        if n & 0x80: GPIO.output(SR_DATA, True)
        else: GPIO.output(SR_DATA, False)
        GPIO.output(SR_SHIFT, True)
        GPIO.output(SR_SHIFT, False)
        n = n << 1
        
def SR_Lock():
    GPIO.output(SR_LOCK, True)
    GPIO.output(SR_LOCK, False)

def b(n): return (1<<n-1) ^ 0xFF

def L1(n, pt):
    base = {
        0: 0xFF & b(4) & b(1) & b(2) & b(8) & b(5) & b(7),
        1: 0xFF & b(2) & b(5),
        2: 0xFF & b(4) & b(2) & b(6) & b(8) & b(7),
        3: 0xFF & b(4) & b(2) & b(6) & b(5) & b(7),
        4: 0xFF & b(1) & b(2) & b(6) & b(5),
        5: 0xFF & b(4) & b(1) & b(6) & b(5) & b(7),
        6: 0xFF & b(4) & b(1) & b(6) & b(8) & b(5) & b(7),
        7: 0xFF & b(4) & b(2) & b(5),
        8: 0xFF & b(1) & b(2) & b(4) & b(5) & b(6) & b(7) & b(8),
        9: 0xFF & b(1) & b(2) & b(4) & b(5) & b(6) & b(7),
    }[n]
    fin = base
    if pt: return base & b(3)
    else: return base

def L2(n, pt):
    base = {
        0: 0xFF & b(4) & b(6) & b(1) & b(8) & b(3) & b(7),
        1: 0xFF & b(1) & b(3),
        2: 0xFF & b(4) & b(1) & b(5) & b(8) & b(7),
        3: 0xFF & b(4) & b(1) & b(5) & b(3) & b(7),
        4: 0xFF & b(6) & b(1) & b(5) & b(3),
        5: 0xFF & b(4) & b(6) & b(5) & b(3) & b(7),
        6: 0xFF & b(4) & b(6) & b(5) & b(3) & b(7) & b(8),
        7: 0xFF & b(1) & b(3) & b(4),
        8: 0xFF & b(1) & b(3) & b(4) & b(5) & b(6) & b(7) & b(8),
        9: 0xFF & b(1) & b(3) & b(4) & b(5) & b(6) & b(7),
    }[n]
    if pt: return base & b(2)
    else: return base

def L(n):
    p1=0;p2=0
    if n<0: p1=1
    n = abs(n)
    n2 = n%10
    n1= (n-n2)/10
    SR_Write(L2(n2, p2))
    SR_Write(L1(n1, p1))
    SR_Lock()

if sys.argv[1] == 'off':
    SR_Write(0xFF)
    SR_Write(0xFF)
    SR_Lock()
    
else: L(int(sys.argv[1]))