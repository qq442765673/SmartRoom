from machine import Pin
led = Pin(15, Pin.OUT)

def Lightcontorl(LightSwitch,AutoLightSwitch,PIR,lighttreahold,lightsens):
    if(LightSwitch==1):
        led.on()
    else:
        led.off()

    if (int(AutoLightSwitch)==1):
        if(int(LightSwitch)==0):
            if(PIR==1):
                print("pir")
                if(lightsens<lighttreahold):
                    print("lightsens<")
                    led.on()
                else:
                    print("lightsens>")
                    led.off()

   