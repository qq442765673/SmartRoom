import _thread
from lisener import listener
from getdata import senddata

import utime



_thread.start_new_thre ad(senddata(),[])
print(1)
listener()
utime.sleep(3)

