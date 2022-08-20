# encoding: utf-8
import socket

class connect_Raspberry():
    def __init__(self,host,port):
        print("客户端开启")
        # 套接字接口
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置ip和端口

        try:
            self.mySocket.connect((host, port))  #连接到服务器
            print("连接到服务器")
        except:  #连接不成功，运行最初的ip
            print('连接RASP不成功')

    def send(self, words):
        # 发送消息
        msg = words
        # 编码发送
        self.mySocket.send(msg.encode("utf-8"))
        print("成功发送消息")

    def close(self):
        self.mySocket.close()
        print("与树莓派丽连接中断\n")
        exit()
        
myRaspConnection = connect_Raspberry('192.168.43.11', 8888)
myRaspConnection.send("hello world") 