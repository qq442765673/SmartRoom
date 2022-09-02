from ctypes import sizeof
from operator import truth
import requests

varId="630a86cf373ded000cec2c0a"
TOKEN="BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk"


s=0 
err=0
c=[100]


def get_var():
    global s
    global err
    # try:
    url = "http://industrial.api.ubidots.com/"
    url = url + \
    "api/v1.6/variables/{0}/values/".format(varId)
    headers = {"X-Auth-Token": TOKEN, }
    req = requests.get(url=url, headers=headers, timeout=3)
    print("satatus:"+str(req.status_code))
    print("delay:"+str(req.elapsed))
    c.append(req.elapsed)
    s=s+1
# except:
    # err=err+1
    # print("get_error")

for i in range(10):
    get_var()

print("succeed"+str(s))
print("error"+str(err))
print(c)
