from socketPico import connect_Pc
import json
import utime


a={"giao":1,"bugiao":2}

data = json.dumps(a)

print(data)

myRaspConnection = connect_Pc('192.168.1.213', 8888)
while 1:
    myRaspConnection.send(data)
    utime.sleep(1)
