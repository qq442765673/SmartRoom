import machine
from light import BH1750
import utime

def lightpro():
    scl = machine.Pin(27)
    sda = machine.Pin(26)
    utime.sleep_ms(100)
    i2c = machine.I2C(1, scl=scl, sda=sda, freq=400001)

    s = BH1750(i2c)
    data= s.luminance(BH1750.ONCE_HIRES_1)
    return data
