import time
import threading


def sing():
    for i in range(10):
        print("Singing...", i)
        time.sleep(1)
        # exit()

def sing1():
    for i in range(10):
        print("SingingSinging...", i)
        time.sleep(1)
        # exit()

if __name__ == '__main__':
    thread_sing = threading.Thread(target=sing)
    thread_sing_1 = threading.Thread(target=sing1)
    thread_sing.setDaemon(True)
    thread_sing_1.setDaemon(True)
    thread_sing.start()
    thread_sing_1.start()

    time.sleep(2)
    print("Over...")
    exit()


