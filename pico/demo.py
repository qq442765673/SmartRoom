from machine import I2C, Pin
import utime
from tempsensor import get
from PIR import PIR
from wifi import wificon
from Ubi import build_payload,post_request
from light1 import lightpro
import _thread
from lisener import listener
from getdata import senddata

def th_func(delay, id):
    while True:
        utime.sleep(delay)
        print('Running thread %d' % id)


_thread.start_new_thread(th_func, [1,1])
th_func(3,0)
