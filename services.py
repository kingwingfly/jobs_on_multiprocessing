from time import sleep, asctime
import subprocess
from job_threads import Message
from jobs import *

# 发任务给pool使执行
def service(pool):
    pool.excute(job1)
    pool.excute(job2)


# 是否meet_time
def meet_time_or_not():
    # asctime()返回如下："Wed Jun  9 04:26:40 1993"
    time_str_list = asctime().split(" ")
    date = time_str_list[0]
    clock = time_str_list[-2][:-3]
    flag_date = False if date in ["Sat, Sun"] else True
    flag_time = True if clock in ["8:00", "20:00"] else False
    return flag_date and flag_time


def check_time(sender_service):
    while True:
        if meet_time_or_not():
            sender_service.send(True)
            # 时间匹配成功后暂停获取时间，提前三分钟再次再次开始
            sleep(12 * 3600 - 1800)
        # 按精度需求调节 60以内
        sleep(1)


def check_net(sender_service):
    # 首次检查需要启动服务
    need_start = True
    while True:
        # 利用ping测试网络连通性，当百度和B站均连不上才认为断网
        ret = subprocess.run(
            "ping baidu.com -n 1",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        flag1 = False if ret.returncode == 200 else True
        ret = subprocess.run(
            "ping baidu.com -n 1",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        flag2 = False if ret.returncode == 200 else True
        # 连通且需要启动服务时
        if (flag1 or flag2) and need_start:
            print("Net connected! Trying to restart service...")
            if meet_time_or_not():  # 若连通网络或者首次启动时，正好到点，则仅由check_time()启动服务
                need_start = False
                continue
            sender_service.send(True)
            # 服务启动后不再需要启动
            need_start = False
        # 未连通
        elif not (flag1 or flag2):
            # 需要重启服务
            need_start = True
            print("Connect Faild! Waiting to restart service...")
        sleep(120)
