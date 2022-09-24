from email import message
from multiprocessing import Process, Pipe
from time import sleep

def foo1():
    print(1)

def foo2():
    print(2)

def wait_run(receiver):
    while True:
        message = receiver.recv()
        message.f()

def excute(foo, sender):
    message = Message(foo)
    sender.send(message)

class Message:
    def __init__(self, fuction):
        self.f = fuction

if __name__ == "__main__":
    # sender1, receiver1 = Pipe()
    # thread1 = Process(target=wait_run, args=(receiver1,))
    # thread1.start()
    # sender2, receiver2 = Pipe()
    # thread2 = Process(target=wait_run, args=(receiver2,))
    # thread2.start()
    # while True:
    #     excute(foo1, sender1)
    #     excute(foo2, sender2)
    t = "Wed Jun  9 04:26:40 1993"
    print(t.split(' '))

