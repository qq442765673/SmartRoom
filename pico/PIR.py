from machine import Pin

def PIR():
    pir = Pin(2,Pin.IN, Pin.PULL_DOWN)
    if pir.value()==1:
        return 1 
    elif pir.value()==0:
        return 0
    else:
        print("pir error")