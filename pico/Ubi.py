import utime
import urequests
import math
import random

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk" 
DEVICE_LABEL = "raspberrypi"  
VARIABLE_LABEL_1 = "temperature"  
VARIABLE_LABEL_2 = "humidity"  
VARIABLE_LABEL_3 = "light"
VARIABLE_LABEL_4 = "motion"
VARIABLE_LABEL_5 = "lightswitch"
VARIABLE_LABEL_6 = "fanswitch"


def build_payload6(value_1, value_2,value_3,value_4,value_5,value_6):

    payload = {VARIABLE_LABEL_1: value_1,
               VARIABLE_LABEL_2: value_2,
               VARIABLE_LABEL_3: value_3,
               VARIABLE_LABEL_4: value_4,
               VARIABLE_LABEL_5: value_5,
               VARIABLE_LABEL_6: value_6

               }
    return payload

def post_request(payload):
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}


    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = urequests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        utime.sleep(0.1)

    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True




