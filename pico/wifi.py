import network
import utime
from machine import Pin

def wificon():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

#     ssid = "VM8610885"
#     pw = "qr7Tgmwht4xv"
    ssid = "jwYo Hyperoptic 1Gb Fibre 2.4Ghz"
    pw = "Tanghaoyue666!"

    wlan.connect(ssid, pw)

    def light_onboard_led():
        led = Pin('LED', Pin.OUT)
        led.on();

    timeout = 10
    while timeout > 0:
        if wlan.status() >= 3:
            light_onboard_led()
            break
        timeout -= 1
        print('Waiting for connection...')
        utime.sleep(1)
       
    wlan_status = wlan.status()
