import machine
from light import BH1750

scl = machine.Pin(27)
sda = machine.Pin(26)
i2c = machine.I2C(1, scl=scl, sda=sda)

s = BH1750(i2c)

while True:
    print(s.luminance(BH1750.ONCE_HIRES_1))
    