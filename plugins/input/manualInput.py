# -*- coding: utf-8 -*-
from plugins import plugin
import time
import feedparser
import globalv
class asyncInput(object):
    def __init__(self,Queue,stop):
        self.Queue=Queue
        print "Oh hai"
        while stop.isSet()==False:
            input=raw_input("input: ")
            print "Adding to queue:",'#'+input
            self.Queue.put('#'+input)
            print "Added to queue!"
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]
