import threading

def execute():
    print("hello")


t=threading.Timer(2,execute)
t.start()
