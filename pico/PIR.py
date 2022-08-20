from machine import Pin
import time

def PIR():
    pir = Pin(2,Pin.IN, Pin.PULL_DOWN)
    led = Pin('LED', Pin.OUT)
    if pir.value()==1:
#         print("someone here")
#         print(pir.value())
#         time.sleep(1)
#         led.on()
#         time.sleep(.2)
#         led.off()
#         time.sleep(.2)
        return 1
   
        
    else:
#         print("nobody")
        time.sleep(1)
        return 0

