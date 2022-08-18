from machine import Pin
import time

pir = Pin(0,Pin.IN, Pin.PULL_DOWN)
led = machine.Pin('LED', machine.Pin.OUT)


while True:
    if pir.value()==1:
        print("someone here")
        print(pir.value())
        time.sleep(1)
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
   
        
    else:
        print("nobody")
        time.sleep(1)
