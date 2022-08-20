from PIR import PIR
from machine import I2C, Pin
import time
led = machine.Pin(15, machine.Pin.OUT)

def pirled():
    pir=PIR()
    print(pir)
    if pir==1:
        led.on()
    else:
        led.off()
    time.sleep(3)
    
pirled()
led.off()

