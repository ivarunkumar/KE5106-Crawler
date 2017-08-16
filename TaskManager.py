from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import threading
from time import sleep
from queue import Queue
import logging

class TaskManager (object) :
    def __init__(self) : 
        self.gThreadPool = ThreadPoolExecutor(10)
    
    def addTask(self, taskFn, callbackFn, args) :
        #self.taskQueue.put(task)
        ft = self.gThreadPool.submit(taskFn, args)
        ft.add_done_callback(callbackFn)
        #logging.debug("Task enqueued")
        print("Task enqueued")