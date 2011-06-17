# -*- coding: utf-8 -*-
#Multithreading IRC bot engine
import time
import random
import Queue
import threading

class inputSystem(object):
    def __init__(self):
        self.processList=[]
        self.Queue=Queue.Queue()
        self.primaryProducer=""
    def addInputSource(self, source, *args):
        if self.getNumActiveSources()>100:
            raise Exception("Too many input sources, possible process-apocalypse detected!")
        inputQueue = Queue.Queue()
        args=(self.Queue, inputQueue)+(args[0] if len(args)>0 else ())
        q=threading.Thread(target=source, args=args)
        if self.primaryProducer=="":
            self.primaryProducer=q
        q.daemon=True
        self.processList.append(q)		
        return inputQueue
    def startInputDaemons(self):
        for process in self.processList:
            if process.is_alive()==False:
                if process.ident==None:
                    process.start()
                else:
                    self.processList.remove(process)
    def getInput(self):
        data=self.Queue.get()
        return data
    def killAll(self):
        for process in self.processList:
            process.terminate()
    def getSources(self):
        return self.processList
    def getNumActiveSources(self):
        x=0
        for process in self.processList:
            if process.is_alive()==True:
                x+=1
        return x

    def getPrimaryProducerStatus(self):
        if self.primaryProducer.is_alive()==True:
            return True
        else:
            return False
