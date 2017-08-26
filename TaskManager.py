from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import threading
from time import sleep
from queue import Queue, Empty
import logging
from selenium import webdriver
import time
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
        
    def worker(self):
        while True:
            try : 
                
                if self.taskQueue.empty() :
                    print(self.gThreadPool._thread_name_prefix, "queue empty. sleeping for 5 secs.")
                    time.sleep(5)
                else:
                    
                    task = self.taskQueue.get(block=False, timeout=100)
                    print ("TaskManager.worker: dequeuing", task.taskName, "Items in queue", self.taskQueue.qsize())
                    if task.taskName == "END_WORKER":
                        print ("TaskManager.worker terminated")
                        break
                    self.addTask(task.taskFn, task.callbackFn, task.taskArgs)
                    self.taskQueue.task_done()
            except Empty as e:
                print(e)
                
    def start(self):
        if (self.dequeThread.is_alive() == False):
            self.dequeThread.start()
            
                        
    def addTask(self, taskFn, callbackFn, args) :
        ft = self.gThreadPool.submit(taskFn, args)
        ft.add_done_callback(callbackFn)
        #print("Task enqueued")
        
    def addTaskQ(self, task):
        self.taskQueue.put(task)
        print("Queuing", task.taskName, "Queue Size", self.taskQueue.qsize());
        
    def shutdown(self):
        if (self.dequeThread.is_alive() == True):
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
        
