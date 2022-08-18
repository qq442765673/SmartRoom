from machine import Pin

data1= Pin(0, Pin.IN ,)
data2= Pin(1, Pin.IN)

print(data1.value())
print('--------------------------')
print(data2.value())