# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
import re
import urllib2
class asyncInput(object):
    def __init__(self,Queue,stop, channel, name):
        self.Queue=Queue
        colour="\x03"
        url="http://www.bakabt.com/user/956181/"+name+".html"
        print "Hello, I am bakabtreader",name," and I am feedreading",channel
        latestFeedItem=""
        checkFrequencies=[10,20,30,60,120,180,240,300]
        lastReadWasBlank=0
        checkFrequency=3
        while stop.isSet()==False:
            try:
                feed=urllib2.urlopen(url).read()
                newFeedItem=re.findall("Share ratio</td>.*?<span.*?>(.*)</span>",feed.replace('\n','').replace('\r',''))[0]
                if newFeedItem!=latestFeedItem:
                    latestFeedItem=newFeedItem
                    Queue.put("#PRIVMSG "+channel+" :\x0312"+name+"\x03's ratio: \x0311"+newFeedItem+"\r\n") 
                    if checkFrequency>0:
                        checkFrequency-=1
                        checkFrequency=0 if checkFrequency<0 else checkFrequency
                else:
                    if checkFrequency<len(checkFrequencies)-1 and lastReadWasBlank:
                        checkFrequency+=1
                        lastReadWasBlank=0
                    lastReadWasBlank=1
                time.sleep(checkFrequencies[checkFrequency])
            except Exception as detail:
                print "Baka Grabbing failure! Bad feed?"
                Queue.put("#PRIVMSG PY :"+name+" shutting down: "+str(detail))
                stop.set()
        Queue.put("#PRIVMSG "+channel+" :RSS Reader "+name+" Shut down.")
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]
