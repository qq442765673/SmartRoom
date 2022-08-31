import Nurequests
import utime
from wifi import wificon

TOKEN = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"  # Put your TOKEN here
DEVICE = "RaspberryPi" # Assign the device label to obtain the variable


def get_var(device, variable):
    i=0
    while i<5:
        try:
            url = "http://industrial.api.ubidots.com/"
            url = url + \
                "api/v1.6/devices/{0}/{1}/".format(device, variable)
            headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
            print("geting: "+variable )
            req = Nurequests.get(url=url, headers=headers,timeout=5)
            print('get '+variable)
            return req.json()['last_value']['value']
            utime.sleep(0.5)
            i=6
        except:
            i=i+1
            print("get error")