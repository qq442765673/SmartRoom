from machine import I2C, Pin
import utime

def check_crc(data):
    crc = 0xFF
    for b in data[:-1]:
        crc ^= b;
        for _ in range(8, 0, -1):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x131;
            else:
                crc <<= 1
    crc_to_check = data[-1]
    # print('crc', crc, 'check', crc_to_check)
    return crc_to_check == crc

sensor = I2C(0, scl=Pin(1), sda=Pin(0), freq=40000)
utime.sleep_ms(100)
addr = 0x44
read_temp_hum_cmd = b'\x2c\x10'

while True:
    # sensor.start()
    sensor.writeto(addr, read_temp_hum_cmd)
    utime.sleep(0.5)
    data = sensor.readfrom(addr,6)
    print(check_crc(data[0:3]))
    print(check_crc(data[3:6]))
    wen = (((data[0] << 8 | data[1]) * 175) / (0xFFFF - 1)) - 45
    rh = (((data[3] << 8 | data[4]) * 100.0) / (0xFFFF - 1))

    print('温度:', wen, '湿度', rh)
    utime.sleep(0.5)