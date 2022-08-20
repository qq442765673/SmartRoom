from machine import Pin
from time import sleep

def fanOn():
    IN1 = Pin(21,Pin.OUT)
    IN2 = Pin(20,Pin.OUT)
    IN3 = Pin(19,Pin.OUT)
    IN4 = Pin(18,Pin.OUT)

    pins = [IN1, IN2, IN3, IN4]

    sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

    # sequence = [[1,0,0,0],[0,0,0,1]]

    while True:
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)
def fanoff():
    IN1 = Pin(21,Pin.OUT)
    IN2 = Pin(20,Pin.OUT)
    IN3 = Pin(19,Pin.OUT)
    IN4 = Pin(18,Pin.OUT)

    pins = [IN1, IN2, IN3, IN4]

#     sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

    sequence = [[1,0,0,0],[0,0,0,1]]

    while True:
        for step in sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep(0.001)