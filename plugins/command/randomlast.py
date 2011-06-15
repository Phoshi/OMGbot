# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import random
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message().strip()
        ttime=time.gmtime()
        result=""
        year=time.gmtime()[0]
        day=time.gmtime()[7]
        results=[]
        channel=complete.channel() if msg=="" else msg
        while not result:
            if not os.path.exists(os.path.join("logs","LogFile - "+channel+"-"+str(year) + "-" + str(day))):
                result="break!"
                break
            with open(os.path.join("logs","LogFile - "+channel+"-"+str(year) + "-" + str(day))) as file:
                text=file.read()
            text=text.split('\n')
            results+=text
            day-=1
            if day==0:
                year-=1
                day=365
        random.shuffle(results)
        result=results[0]
        return ["PRIVMSG $C$ :"+result]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !last module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!last [phrase]"]
