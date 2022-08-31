from re import I
import time

c=[3]
i=0
while 1:
    try:
            i=i+1
            print(i)
            time.sleep(1)
            c[i]=3
    except:
        print("error")  


