from machine import I2C, Pin
import utime
from tempsensor import get
from PIR import PIR
from Ubi import build_payload6,post_request
from light1 import lightpro
from socketPico import connect_Pc
import json

led = Pin('LED', Pin.OUT)

def senddata(wh,light,pir,lightswitch,funswitch):  

    payload=build_payload6(wh[0],wh[1],light,pir,lightswitch,funswitch)
    post_request(payload)
    
    data = json.dumps(payload)
    i=0
    while i<3:
        try:
            myRaspConnection = connect_Pc('192.168.1.213', 8888)
            myRaspConnection.send(data)
            i=4
        except:
            i=i+1
            print("get error")
    utime.sleep(0.001)

