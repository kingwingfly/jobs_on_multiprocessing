from multiprocessing import Process, Lock
from multiprocessing.connection import Pipe
# 使线程处于持续接收message的状态
def wait_to_work(id, receiver, mutex):
    while True:
        #由于有多个sender向receiver发送message，故锁
        mutex.acquire()
        message = receiver.recv()
        mutex.release()
        if not message.terminate:
            print(f"Worker {id} got a job; executing.")
            message.job()
        # 如果message.terminate为True，则结束这个进程
        else:
            print(f"Worker {id} was told to terminate.")
            break

class Message:
    def __init__(self, job, terminate = False):
        self.terminate = terminate  # 是否终止进程
        self.job = job  # job存入message

class Worker:
    def __init__(self, id, receiver, mutex):
        self.id = id
        # 每个workr有id，负责一个thread
        self.thread = Process(target = wait_to_work, args = (id, receiver, mutex,))
        self.thread.start()

class ThreadPool:
    def __init__(self, size):
        assert(size > 0, "The size of the ThreadPool is illegal!")
        self.mutex = Lock() # 为线程池中的线程准备的互斥锁
        self.sender, self.receiver = Pipe()
        self.workers = []
        for id in range(size):
            worker = Worker(id, self.receiver, self.mutex)
            self.workers.append(worker)
    # 发任务给worker手中的thread
    def excute(self, job):
        message = Message(job)
        self.sender.send(message)