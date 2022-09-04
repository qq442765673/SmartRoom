import machine


i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))


devices = i2c.scan()
if devices:
    for d in devices:
        print(hex(d))