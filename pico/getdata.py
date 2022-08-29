from machine import I2C, Pin
import utime
from tempsensor import get
from PIR import PIR
from wifi import wificon
from Ubi import build_payload6,post_request
from light1 import lightpro
from socketPico import connect_Pc
import json

led = Pin('LED', Pin.OUT)

wificon()
def senddata(funswitch):
    wh=get()
    print(wh[0])
    print(wh[1])

    pir=PIR()
    print(pir)

    light=lightpro()

    print(light)
    
    lightswitch=led.value()
    

    payload=build_payload6(wh[0],wh[1],light,pir,lightswitch,funswitch)
    post_request(payload)
    
    data = json.dumps(payload)
    myRaspConnection = connect_Pc('192.168.1.213', 8888)
    myRaspConnection.send(data)
    utime.sleep(0.001)

