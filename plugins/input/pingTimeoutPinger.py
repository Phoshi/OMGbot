# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
import re
import urllib2

class asyncInput(object):
    def __init__(self,Queue,stop):
        self.Queue=Queue
        while stop.isSet()==False:
            Queue.put("#") 
            time.sleep(60)
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]
