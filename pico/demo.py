from machine import Pin
import time
led = machine.Pin(15, machine.Pin.OUT)

while (True):
    led.on()
    time.sleep(.2)
    led.off()
    time.sleep(.2)
   
