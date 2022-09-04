from audioop import avg
from re import S
from turtle import delay
import requests
import random
import time
import pandas as pd

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable
autofanId="autofan"
autolightId="autolight"
lightswitchId = "lightswitch"
fanswitchId= "fanswitch"

s=0 
err=0


def test_var(device, variable):
    delay1=[]
    for i in range(100):
        global s
        global err
        try:
            url = "http://industrial.api.ubidots.com/"
            url = url + \
                "api/v1.6/devices/{0}/{1}/".format(device, variable)
            headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
            req = requests.get(url=url, headers=headers, timeout=10)
            print('get '+variable )
            print("satatus:"+str(req.status_code))
            print("delay:"+str(req.elapsed))
            a=str(req.elapsed)[5:]
            delay1.append(float(a))
            s=s+1
        except:
            err=err+1
            print("timeout")  
    return delay1
        


delay2= test_var(DEVICE,autofanId)
delay3= test_var(DEVICE,autolightId)
delay4= test_var(DEVICE,lightswitchId)
delay5= test_var(DEVICE,fanswitchId)
delay2.append(sum(delay2)/len(delay2))
delay3.append(sum(delay3)/len(delay3))
delay4.append(sum(delay4)/len(delay4))
delay5.append(sum(delay5)/len(delay5))
data = pd.DataFrame({autofanId:delay2,autolightId:delay3,lightswitchId:delay4,fanswitchId:delay5})
data.to_excel("evaluation.xlsx",sheet_name='sheet1',index=False)
