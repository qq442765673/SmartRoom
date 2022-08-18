from machine import Pin
import time
motor = Pin(0, Pin.OUT,)
motor.value(1)
while (True):
    time.sleep(.2)
    print(motor.value())

