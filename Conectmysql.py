import time
import mysql.connector

def picomysql(Temperature,Humidity,Light,Motion,LightSwitch,FanSwitch):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="442765673",
        database="raspberrypi"
    )

    mycursor = mydb.cursor()

    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    sql = "INSERT INTO raspberrypi (tempureture, humidity,light,motion,lightswitch,fanswitch,times) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (Temperature,Humidity,Light,Motion,LightSwitch,FanSwitch,localtime)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


