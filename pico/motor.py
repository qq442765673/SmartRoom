from machine import Pin
import time
motor1 = Pin(0, Pin.OUT)
motor2 = Pin(1, Pin.OUT)
while (True):
    motor1.value(1)
    motor2.value(0)
    time.sleep(.2)
    print(motor1.value())

