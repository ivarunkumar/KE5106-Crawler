from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import threading
from time import sleep
from queue import Queue
import logging

WORKER_COUNT=10
threadPool = ThreadPoolExecutor(WORKER_COUNT)

def addTask(taskFn, callbackFn, args) :
    #self.taskQueue.put(task)
    ft = threadPool.submit(taskFn, args)
    ft.add_done_callback(callbackFn)
    #logging.debug("Task enqueued")
    print("Task enqueued")
             
        


    
import threading
import time
import Queue
def consume(q):
    while(True):
        name = threading.currentThread().getName()
        print "Thread: {0} start get item from queue[current size = {1}] at time = {2} \n".format(name, q.qsize(), time.strftime('%H:%M:%S'))
        item = q.get();
        time.sleep(3)  # spend 3 seconds to process or consume the tiem
        print "Thread: {0} finish process item from queue[current size = {1}] at time = {2} \n".format(name, q.qsize(), time.strftime('%H:%M:%S'))
        q.task_done()


def producer(q):
    # the main thread will put new items to the queue

    for i in range(10):
        name = threading.currentThread().getName()
        print "Thread: {0} start put item into queue[current size = {1}] at time = {2} \n".format(name, q.qsize(), time.strftime('%H:%M:%S'))
        item = "item-" + str(i)
        q.put(item)
        print "Thread: {0} successfully put item into queue[current size = {1}] at time = {2} \n".format(name, q.qsize(), time.strftime('%H:%M:%S'))

    q.join()

if __name__ == '__main__':
    q = Queue.Queue(maxsize = 3)

    threads_num = 3  # three threads to consume
    for i in range(threads_num):
        t = threading.Thread(name = "ConsumerThread-"+str(i), target=consume, args=(q,))
        t.start()

    #1 thread to procuce
    t = threading.Thread(name = "ProducerThread", target=producer, args=(q,))
    t.start()

    q.join()







from random import randint
 
def return_after_5_secs(num):
    v=randint(3, 15)
    print("Thread #{} Sleeping for {} secs".format(num, v))
    sleep(v)
    #print("Return of {}".format(num))
    return "Return of {}".format(num)
 
def callback(ftr):
    print("At callback {}".format(ftr.result()))
    threadPool.submit(return_after_5_secs, 100)
    


futures = []
for x in range(20):
    ft = threadPool.submit(return_after_5_secs, x)
    ft.add_done_callback(callback)
    futures.append(ft)
wait(futures)
for future in futures:
    print(future.result())    