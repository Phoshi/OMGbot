# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
class asyncInput(object):
    def __init__(self,Queue,stop,X,destination, channel):
        self.Queue=Queue
        if len(destination.split('|'))==1:
            hasDate=0
        else:
            hasDate=1
        while stop.isSet()==False:
            currentTime=time.strftime("%H:%M|%d-%m-%y") if hasDate else time.strftime("%H:%M")
            if destination==currentTime:
                Queue.put("#PRIVMSG "+channel+" :"+X+"\r\n")
                stop.set()
            time.sleep(60)
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I SAY X EVERY Y"]
