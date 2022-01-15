import time
import threading


aa = 0
bb = 0

def work1():
    global aa
    for i in range(1000000):
        lock1.acquire()
        aa += 1
        lock1.release()
    print("Work1....", aa)


def work2():
    global aa
    for i in range(1000000):
        lock1.acquire()
        aa += 1
        lock1.release()
    print("Work2....", aa)


def work3():
    global bb
    for i in range(1000000):
        bb += 1
    print("Work3....", bb)


if __name__ == "__main__":
    t1 = threading.Thread(target=work1)
    t2 = threading.Thread(target=work2)
    t3 = threading.Thread(target=work3)
    lock1 = threading.Lock()


    t1.start()
    t2.start()
    t3.start()

    while len(threading.enumerate()) != 1:
        print(len(threading.enumerate()))
        time.sleep(1)
    print("Main....", aa)

