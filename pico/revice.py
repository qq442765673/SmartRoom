import urequests
import random
import time

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable
VARIABLE = "temperature"  # Assign the variable label to obtain the variable value
DELAY = 1  # Delay in seconds

def get_var(device, variable):
#     try:
    url = "http://industrial.api.ubidots.com/"
    url = url + \
        "api/v1.6/devices/{0}/{1}/".format(device, variable)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    req = urequests.get(url=url, headers=headers)
    print('get')
    return req.json()['last_value']['value']
#     except:
#         pass


if __name__ == "__main__":
    while True:
        print(get_var(DEVICE, VARIABLE))
        time.sleep(DELAY)