# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
import urllib2
import json
import Queue
import traceback
from pluginFormatter import formatOutput

class asyncInput(object):
    def __init__(self,outputQueue, inputQueue):
        running = True
        self.Queue=outputQueue
        urlQueue = Queue.Queue()
        globalv.communication["urlFollowQueue"] = urlQueue

        while running:
            while not inputQueue.empty():
                data = inputQueue.get()
                if data == "stop":
                    running = False
            newData = urlQueue.get()
            complete, outputFunction = newData
            try:
                returnData = formatOutput(outputFunction(complete), complete)[0]
                if returnData!="":
                    outputQueue.put("#%s\r\n"%returnData)
            except:
                print "urlFollowd failued:",complete.complete()

            
        del globalv.communication["urlFollowQueue"]
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I SAY X EVERY Y"]
