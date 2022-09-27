"""
Two jobs run depending on date, time and network situation.
2022.9.24
@Louis翔
分不清线程和进程，你懂我意思吧。。。
"""

from multiprocessing.connection import Pipe
from job_threads import ThreadPool
from multiprocessing import Process, Lock
from services import check_time, check_net, service


if __name__ == "__main__":
    pool = ThreadPool(2)  # 建立线程池，2个线程
    sender_service, receiver_service = Pipe()  # 建立主线程和子线程之间的通道
    mutex_service = Lock()  # 为receiver_service准备互斥锁
    thread_check_time = Process(target=check_time, args=(sender_service))
    thread_check_net = Process(target=check_net, args=(sender_service))
    thread_check_time.start()
    thread_check_net.start()
    while True:
        # 可能存在多个sender同时发信息，故锁
        mutex_service.acquire()
        flag = receiver_service.recv()
        mutex_service.release()
        if flag:
            service(pool)
