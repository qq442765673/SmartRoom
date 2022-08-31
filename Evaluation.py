import requests
import random
import time

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable
autofanId="autofan"
autolightId="autolight"
lightswitchId = "lightswitch"
funswitchId= "fanswitch"


def get_var(device, variable):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers, timeout=1)
        print('get '+variable )
        return req.json()['last_value']['value']
    except:
        print("get_error")

for i in range(10):
    get_var(DEVICE,autofanId)
