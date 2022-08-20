import time
from machine import I2C, Pin
import utime
from tempsensor import get
from PIR import PIR
from wifi import wificon
from Ubi import build_payload,post_request
from light1 import lightpro

timesleep = 120
wificon()
while 1 :

    wh=get()
    print(wh[0])
    print(wh[1])

    pir=PIR()
    print(pir)

    light=lightpro()

    print(light)


    lightswitch=1

    funswitch=1

    payload=build_payload(wh[0],wh[1],light,pir,lightswitch,funswitch)
    post_request(payload)
    time.sleep(timesleep)

