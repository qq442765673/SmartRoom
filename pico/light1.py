import machine
import light
from light import BH1750

scl = machine.Pin(1)
sda = machine.Pin(0)
i2c = machine.I2C(0, scl=scl, sda=sda)

s = BH1750(i2c)

while True:
    s.luminance(BH1750.ONCE_HIRES_1)
    s.luminance(BH1750.ONCE_HIRES_1)
