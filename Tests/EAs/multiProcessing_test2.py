## what I want:
# a main thread: initialise children, and a queue/pipe for each childe.
# Each child:
    # execute a method, then waits for queue. When something in queue: run method (eval) with
    # queueitems as arguments, and sets a value in the queueItems-object.
# the main thread has acess to these queueItems and there values.
# after this: the main thread can set new objects in the queues, and the children will run the eval again


import multiprocessing
import os
import time
from multiprocessing.managers import BaseManager, NamespaceProxy
import copy


class valueContainer():
    def __init__(self):
        
        self.value = 0
        self.finishFlag = 0

    def getValue(self):
        return self.value

    def setValue(self,x):
        #print(self.name, "Setting value",x)
        time.sleep(1)
        self.value = x
        print("value set",x)

    def setFinishFlag(self):
        self.finishFlag=1
        print("finishFlag set")
    
    def getFinishFlag(self):
        return self.finishFlag


def worker_main(queue):
    print(os.getpid(),"working")
    while True:
        item = queue.get(block=True) #block=True means make a blocking call to wait for items in queue
        if item is None:
            break
        
        #if type(item)==list:
        for el in item:
        #the operation
            el.value=1
            #el.setFinishFlag()
            print("her:",el.getValue())
            el.finishFlag = 1
            print(el.getValue(),"job done",el.getFinishFlag())
        #else:
        #   print(type(item))
        #    sys.exit("item is not list")

def defineList(NUM_QUEUE_LISTS, NR_OBJ, manager):
    queueObjects=[]#manager.list()
    for i in range(NUM_QUEUE_LISTS):
        aListOfObj = []#manager.list()
        for j in range(NR_OBJ):
            obj = manager.valueContainer()
            aListOfObj.append(obj)
            print("before:",obj.getValue())
        queueObjects.append(aListOfObj)
    return queueObjects

def addToQueue(NUM_QUEUE_LISTS, objects, the_queue):
    for i in range(NUM_QUEUE_LISTS):
        the_queue.put(objects[i])

def checkIfDone(objects, NR_OBJ):
    # check that the the queue is empty and the job is done....need a join() - that does not end the process
    

    #print("checking if queue is empty") # but we need to check that the job is done instead
    while not the_queue.empty():
        time.sleep(1)
    #print("empty")
    for i in range(NR_OBJ):
        finishedFlagSet(objects[i])    


def finishedFlagSet(list):
    #for el in list:
    print("hhhhh",[el.getFinishFlag() for el in list])
    while not all(el.getFinishFlag()==1 for el in list):
        time.sleep(1)
        print("sleeping", list[0].getFinishFlag())
    print([el.getFinishFlag() for el in list])


class MyManager(BaseManager): pass

class IndProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')

    # to add a method:
    #_exposed_ = ('__getattribute__', '__setattr__', '__delattr__','getValue')

    #def getValue(self):
    #    callmethod = object.__getattribute__(self, '_callmethod')
    #    return callmethod('getValue')


def main():
    NUM_PROCESSES = 1
    NUM_QUEUE_LISTS = 2 
    NR_OBJ = 2
    generations = 1
    #original
    #BaseManager.register('valueContainer', valueContainer)
    #manager = BaseManager()
    #manager.start()
    
    #new
    MyManager.register('valueContainer', valueContainer, IndProxy)
    manager = MyManager()
    manager.start()

    #manager = multiprocessing.Manager()
    the_queue = multiprocessing.Queue()
    the_pool = multiprocessing.Pool(NUM_PROCESSES, worker_main,(the_queue,))


    print("starting")
    for g in range(generations):
        list= defineList(NUM_QUEUE_LISTS, NR_OBJ, manager)
        addToQueue(NUM_QUEUE_LISTS, list, the_queue)
        time.sleep(5)
        print(list[0][0].getValue(), list[0][1].getValue(), list[1][0].getValue(), list[1][1].getValue())
        checkIfDone(list, NR_OBJ)



    print("Done")
    for i in range(NUM_QUEUE_LISTS):
        the_queue.put(None)
    # prevent adding anything more to the queue and wait for queue to empty
    the_queue.close()
    the_queue.join_thread()

    # prevent adding anything more to the process pool and wait for all processes to finish
    the_pool.close()
    the_pool.join()



if __name__ == '__main__':
    
    #main()

    a=valueContainer()
    a.value=45
    b=copy.copy(a)
    b.value=80

