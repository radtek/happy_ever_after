# import os
import time
import psutil
import yagmail


def info_get(time_interval):
    cpu_total = psutil.cpu_count(logical=False)
    cpu_usage = psutil.cpu_percent(interval=time_interval)
    mem_info = psutil.virtual_memory()
    mem_total = mem_info.total // (1024 ** 3)
    mem_usage = mem_info.percent
    disk_info = psutil.disk_usage("/")
    disk_total = disk_info.total // (1024 ** 3)
    disk_usage = disk_info.percent
    net_info = psutil.net_io_counters()
    net_in_info = net_info.bytes_recv
    net_out_info = net_info.bytes_sent

    cur_time = time.strftime("%Y%m%d %H:%M:%S")

    log_str  = '|-----------------------|---------------|---------------|---------------|-------------------------------|\n'
    log_str += '|TIME\t\t\t|CPU_USAGE\t|MEM_USAGE\t|DISK_UASGE\t|NET_INFO\t\t\t|\n'
    log_str += '|\t\t\t|(total: %dC)\t|(total: %d G)\t|(total: %dG)\t|\t\t\t\t|\n' % (cpu_total, mem_total, disk_total)
    log_str += '|-----------------------|---------------|---------------|---------------|-------------------------------|\n'
    log_str += '|%s\t|%s%%\t\t|%s%%\t\t|%s%%\t\t|In:%d/Out:%d\t|\n' % (cur_time, cpu_usage, mem_usage, disk_usage, net_in_info, net_out_info)
    log_str += '|-----------------------|---------------|---------------|---------------|-------------------------------|\n'

    print(log_str)

    f = open("log.txt", 'a')
    f.write(log_str)
    f.close()
    # os.remove("log.txt")

    if cpu_usage > 80 or mem_usage > 20:
        yag_obj.send("cnwn1111@163.com", "This is a notification", log_str)
        # yag_obj.send(to=("cnwn1111@163.com", subject="cnwn1111@hotmail.com"), contents="This is a notification", log_str)
        ## 如果contents=["line a", "line b", "line c"]，则内容会显示成3行
    else:
        print("Donot need to send notification...")

if __name__ == "__main__":
    yag_obj = yagmail.SMTP(user="TEST@163.com", password="PASSWD", host="smtp.163.com")

    while True:
        info_get(5)