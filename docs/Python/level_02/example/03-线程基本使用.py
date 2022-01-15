"""
子线程创建的步骤：
1、导入模块 threading
2、使用threading.Thread() 创建对象（子线程对象）
3、指定子线程执行的分支
4、启动子线程 线程对象.start()
"""

import time
import threading

def sorry():
    time.sleep(2)
    print("Sorry Sorry Sorry")
    print(threading.current_thread())


if __name__ == "__main__":
    for i in range(5):
        thread_obj = threading.Thread(target=sorry)
        thread_obj.start()
        time.sleep(0.5)

    print(len(threading.enumerate()))
    print(threading.current_thread())
    print("===End===")