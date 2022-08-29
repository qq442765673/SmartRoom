from machine import I2C, Pin
import utime
from tempsensor import get
from PIR import PIR
from wifi import wificon
from Ubi import build_payload6,post_request
from light1 import lightpro
from getdata import senddata
from revice import get_var
from FanControl import Fancontorl
from tempsensor import get
from LightControl import Lightcontorl


DEVICE = "RaspberryPi" 
autofanId="autofan"
autolightId="autolight"
lightswitchId = "lightswitch"
funswitchId= "fanswitch"



LightSwitch=0
FanSwitch=0
AutoLightSwitch=0
AutoFanSwitch=0
temptreahold=20
lighttreahold = 0.84

count=0

wificon()

while(1):
    LightSwitch=get_var(DEVICE,lightswitchId)
    FanSwitch=get_var(DEVICE,funswitchId)
    AutoLightSwitch=get_var(DEVICE,autolightId)
    AutoFanSwitch=get_var(DEVICE,autofanId)
    PIRvalue=PIR()
    lightvalue=lightpro()
    wh=get()

    Fancontorl(FanSwitch,AutoFanSwitch,PIRvalue,temptreahold,wh[0])
    Lightcontorl(LightSwitch,AutoLightSwitch,PIRvalue,lighttreahold,lightvalue)

    count = count+1
    if(count>2):
        print(count)
        senddata(FanSwitch);
        count=0
        

        

