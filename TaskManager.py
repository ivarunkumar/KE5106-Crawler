from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import threading
from time import sleep
from queue import Queue
import logging
from selenium import webdriver

class Task :
    def __init__(self, taskName, taskfn, callbackfn, args):
        self.taskName = taskName 
        self.taskFn = taskfn
        self.callbackFn = callbackfn
        self.taskArgs = args
         
class TaskManager (object) :
    def __init__(self, poolName, threadCount=10) : 
        self.gThreadPool = ThreadPoolExecutor(threadCount, poolName)
        self.taskQueue = Queue()
        self.dequeThread = threading.Thread(target=self.worker)
        self.dequeThread.start()
        
    def worker(self):
        while True:
            #q.get() blocks the thread
            task = self.taskQueue.get()
            print ("TaskManager.worker: dequeuing", task.taskName)
            if task.taskName == "END_WORKER":
                print ("TaskManager.worker terminated")
                break
            self.addTask(task.taskFn, task.callbackFn, task.taskArgs)
            self.taskQueue.task_done()
                        
    def addTask(self, taskFn, callbackFn, args) :
        ft = self.gThreadPool.submit(taskFn, args)
        ft.add_done_callback(callbackFn)
        #print("Task enqueued")
        
    def addTaskQ(self, task):
        self.taskQueue.put(task)
        print("Queuing", task.taskName, "Queue Size", self.taskQueue.qsize());
        
    def cleanUp(self):
        self.dequeThread.join()
        self.gThreadPool.shutdown()
        
class BrowserTaskManager (TaskManager):
    
    def __init__(self, poolName, threadCount=10) : 
        super(BrowserTaskManager, self).__init__(poolName, threadCount)
        self.drivers=[]
        for i in range(threadCount) :
            driver = webdriver.Chrome()
            self.drivers.append(driver)
            
    def getDriver(self, index): 
        return self.drivers[index] 
        
