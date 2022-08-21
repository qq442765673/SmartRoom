from wifi import wificon
from revice import get_var
from light1 import lightpro
from PIR import PIR
from tempsensor import get
from motor import fanOn,fanoff
from machine import I2C, Pin
import utime

led = Pin(15, Pin.OUT)

wificon()
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable
VARIABLE = "temperature"  # Assign the variable label to obtain the variable value
lightswitch = "lightswitch"
funswitch= "funswitch"
lighttreahold = 0.84
temptreahold = 20
PIR=PIR()

def listener():
        light=get_var(DEVICE,lightswitch)
        fan=get_var(DEVICE,funswitch)
        wh=get()
        
        if (light==1):
            if(PIR==1):
                if(lightpro()>lighttreahold):
                    led.on()
                    print("ledon")
            else:
                led.off()
#         if (fan==1):
#             if(PIR==1):
#                 if(wh[0]>temptreahold):
#                     fanOn();
#             else:
#                 fanoff();
utime.sleep(1)