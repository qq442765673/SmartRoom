import _thread
import utime


def print_time(thread_name, delay):
 
    count = 0
    while count < 5:
        utime.sleep(delay)
        count += 1
        print("%s: %s" % (thread_name, utime.time()))

_thread.start_new_thread(print_time, ("Thread-2", 4,))
print_time("Thread-1",2)

        
