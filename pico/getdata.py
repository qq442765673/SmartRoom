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
    myRaspConnection = connect_Pc('192.168.1.213', 8888)
    myRaspConnection.send(data)
    utime.sleep(0.001)

