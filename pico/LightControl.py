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
                if(lightsens<lighttreahold):
                    led.on()
                else:
                    led.off()

   