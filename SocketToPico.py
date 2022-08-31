import socket
from tokenize import Double
from turtle import st
import re
import Conectmysql


print ("服务开启")
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.1.213'
port = 8888
Temperature=0
mySocket.bind((host, port))
mySocket.listen(10)
print ("等待连接")
# client,address = mySocket.accept()
str=''
if __name__ == '__main__':
    while True:
        client,address = mySocket.accept()
        while True:
            try:
                data = client.recv(1024)
                print(data.decode("utf-8"))
                str=data.decode("utf-8")
                client.close()
                try:
                    Light = re.search('light\":(.+?),', str).group(1)
                    print(Light)
                except AttributeError:
                    pass

                try:
                    LightSwitch = re.search('lightswitch\":(.+?),', str).group(1)
                    print(LightSwitch)
                except AttributeError:
                    pass

                try:
                    FanSwitch = re.search('funswitch\":(.+?),', str).group(1)
                    print(FanSwitch)
                except AttributeError:
                    pass

                try:
                    Motion = re.search('motion\":(.+?),', str).group(1)
                    print(Motion)
                except AttributeError:
                    pass
                try:
                    Humidity = re.search('humidity\":(.+?),', str).group(1)
                    print(Humidity)
                except AttributeError:
                    pass
                try:
                    Temperature = re.search('temperature\":(.+?)}', str).group(1)
                    Temperature=float(Temperature)
                    print(Temperature)

                except AttributeError:
                    pass

                if Temperature>1:
                    Conectmysql.picomysql(Temperature,Humidity,Light,Motion,LightSwitch,FanSwitch)
                    break
            except Exception:
                break
        client.close()



