import _thread
from machine import I2C, Pin
import utime
from tempsensor import get
from PIR import PIR
from wifi import wificon
from Ubi import build_payload,post_request
from light1 import lightpro
from lisener import listener
from getdata import senddata

count=0
now=utime.time()
while(1):
    listener()
    utime.sleep(1)
    currenttime=utime.time()
    print(now)
    disp=currenttime-now;
    count = count+1
    if(disp%10==0):
        senddata();
        print(count)

        

