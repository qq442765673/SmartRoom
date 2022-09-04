# encoding: utf-8
import socket
import utime

class connect_Pc():
    def __init__(self,host,port):
        print("Client open")

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        try:
            self.mySocket.connect((host, port))  
            print("Connect succeed")
        except:  
            print('Connect fail')

    def send(self, words):

        msg = words

        self.mySocket.send(msg.encode("utf-8"))
        print("Send to Pc succeed")

    def close(self):
        self.mySocket.close()
        print("Disconnected with PC\n")
        exit()
        
