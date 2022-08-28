import urequests
import random
import time
from wifi import wificon

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable

wificon()
def get_var(device, variable):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = urequests.get(url=url, headers=headers)
        print('get '+variable )
        return req.json()['last_value']['value']
    except:
        print("get_error")


