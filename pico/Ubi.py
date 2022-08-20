import time
import urequests
import math
import random

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE_LABEL = "raspberrypi"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
VARIABLE_LABEL_3 = "light"
VARIABLE_LABEL_4 = "motion"
# VARIABLE_LABEL_5 = "lightswitch"
# VARIABLE_LABEL_6 = "funswitch"


def build_payload(value_1, value_2,value_3,value_4):
    # Creates two random values for sending data

    # Creates a random gps coordinates

    payload = {VARIABLE_LABEL_1: value_1,
               VARIABLE_LABEL_2: value_2,
               VARIABLE_LABEL_3: value_3,
               VARIABLE_LABEL_4: value_4

               }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP urequests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP urequests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = urequests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        4, 3, 2,1 )

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")

