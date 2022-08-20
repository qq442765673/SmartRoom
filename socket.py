import socket
import time


print ("服务开启")
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.43.11'
port = 8888

mySocket.bind((host, port))
mySocket.listen(10)

if __name__ == '__main__':
    while True:
        print ("等待连接")
        client,address = mySocket.accept()
        print ("新连接")
        print ("IP is %s" % address[0])
        print ("port is %d\n" % address[1])
        while True:
            msg = 0
            msg = client.recv(1024)
            msg = msg.decode("utf-8")
            if msg != 0:
                print (msg)
                print ("读取完成")
