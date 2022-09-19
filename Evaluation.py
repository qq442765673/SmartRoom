from audioop import avg
from re import S
from turtle import delay
import requests
import random
import time
import pandas as pd

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable
lightId="light"
humidityId="humidity"
motionId = "motion"
temperatureId= "temperature"

s=0 
err=0


def test_var(device, variable):
    delay1=[]
    for i in range(500):
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
        


delay2= test_var(DEVICE,lightId)
delay3= test_var(DEVICE,humidityId)
delay4= test_var(DEVICE,motionId)
delay5= test_var(DEVICE,temperatureId)
delay2.append(sum(delay2)/len(delay2))
delay3.append(sum(delay3)/len(delay3))
delay4.append(sum(delay4)/len(delay4))
delay5.append(sum(delay5)/len(delay5))
data = pd.DataFrame({lightId:delay2,humidityId:delay3,motionId:delay4,temperatureId:delay5})
data.to_excel("androidEvaluation500.xlsx",sheet_name='sheet1',index=False)
