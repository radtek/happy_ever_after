import time
import threading


aa = 0


def work1():
    global aa
    for i in range(10):
        aa += 1
        time.sleep(0.5)
        print("Work1...", aa)


def work2():
    for i in range(5):
        time.sleep(1)
        print("Work2...", aa)


if __name__ == "__main__":
    thread_work1 = threading.Thread(target=work1)
    thread_work2 = threading.Thread(target=work2)

    thread_work1.start()
    thread_work2.start()

    while len(threading.enumerate()) != 1:
        print(len(threading.enumerate()))
        time.sleep(1)
        print(len(threading.enumerate()))
