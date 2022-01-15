import time


def sing():
    for i in range(3):
        print("Singing...")
        time.sleep(0.5)


def dance():
    for i in range(3):
        print("Dancing...")
        time.sleep(0.5)


def sorry():
    for i in range(5):
        print("Sorry [%d]" % i)


if __name__ == "__main__":
    sing()
    dance()
    sorry()