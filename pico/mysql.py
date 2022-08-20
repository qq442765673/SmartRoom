import pymysql

import Adafruit_DHT
import time


con = pymysql.connect(host='192.168.0.67',port=3306,user='root',db='raspberrypi',passwd='442765673')#远程连接MYSQL

cur = con.cursor()#创建游标


while True:
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failure,Try again!')
        break
    time.sleep(1)                 # 延时1s

    sql="insert into raspberrypi values(%s,%s)"
    #由于上传数据只能是字符串，所以这里进行强制转换
    insert=cur.executemany(sql,[(str(31),str(31),str(31),str(1),str(1),str(1))])
    print('sucess',insert)
cur.close()
con.commit()
con.close()