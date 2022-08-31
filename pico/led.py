from machine import Pin
import utime
led = machine.Pin('LED', machine.Pin.OUT)

while (True):
    led.on()
    utime.sleep(.2)
    led.off()
    utime.sleep(.2)
   