from PIR import PIR
from machine import I2C, Pin
import utime
led = machine.Pin(15, machine.Pin.OUT)

def pirled():
    pir=PIR()
    print(pir)
    if pir==1:
        led.on()
    else:
        led.off()
    
while 1:
    pirled()
    utime.sleep(1)
led.off()

