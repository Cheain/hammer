# a test for threading
import threading
import time

i = 0
lock = threading.Lock


def abc():
    while True:
        global i
        i += 1
        print(i)
        print('>>>>', threading.activeCount())
        time.sleep(0.5)


for b in range(100):
    t = threading.Thread(target=abc)
    t.start()
    print('>>>>', threading.activeCount())
