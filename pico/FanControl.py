from motor import fanOn

def Fancontorl(funswitch,autofan,PIR,temptreahold,wh):
    if(funswitch==1):
        fanOn();

    if (int(autofan)==1):
        if(int(funswitch)==0):
            if(PIR==1):
                if(wh>temptreahold):
                    fanOn();

   
