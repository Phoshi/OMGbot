# -*- coding: utf-8 -*-
from plugins import plugin
from SMFThreadInformation import SMFThread
import time
import feedparser
import globalv
class asyncInput(object):
    def __init__(self,Queue, inputQueue):
        self.Queue=Queue
        colour="\x03"
        latestFeedItem=""
        feedName="forum.metroidconstruction.com/index.php?type=rss;action=.xml"
        checkFrequencies=[10,20,30,60,120,180,240,300]
        lastReadWasBlank=0
        checkFrequency=3
        channels = []
        feed=feedparser.parse("http://"+feedName)
        latestFeedItem=feed.entries[0].id
        running = True
        while running:
            while not inputQueue.empty():
                data = inputQueue.get()
                if data.split()[0]=="add":
                    channels.append(data.split()[1])
                    Queue.put("#PRIVMSG %s :MetConst reader starting up\r\n"%data.split()[1])

            try:
                feed=feedparser.parse("http://"+feedName)
                newFeedItem=feed.entries[0].id
                newItems=[]
                if newFeedItem!=latestFeedItem:
                    iterateBack=0
                    while (feed.entries[iterateBack].id!=latestFeedItem and iterateBack<len(feed.entries)-1 and iterateBack < 5):
                        newItems.append ((feed.entries[iterateBack].link, feed.entries[iterateBack].title))
                        iterateBack+=1
                    latestFeedItem=newFeedItem
                    for item in newItems:
                        try:
                            thread=SMFThread(item[0])
                            posterName=thread.thread['entriesByID'][thread.postID]['name']
                            posterName=posterName[0]+"\x03\x0311"+posterName[1:]
                            for channel in channels:
                                Queue.put("#PRIVMSG "+channel+" :\x0312"+name+"\x03:\x0311 "+posterName+"\x03 posted in \x0311"+thread.thread['thread']['title']+"\x03 in \x0311"+thread.thread['thread']['linktree'][-1]+"\x03 (at \x0312"+item[0]+"\x03)\r\n")
                        except Exception as detail:
                            print "MetConst Reader Failed:", detail
                            for channel in channels:
                                Queue.put("#PRIVMSG "+channel+" :\x0312"+name+"\x03:\x0311 "+item[1]+"\x03 (at \x0312"+item[0]+"\x03)\r\n")
                    if checkFrequency>0:
                        checkFrequency-=len(newItems)
                        checkFrequency=0 if checkFrequency<0 else checkFrequency
                        print "Got a lot of items that time. Upping check frequency to",checkFrequencies[checkFrequency],"seconds."
                    
                if len(newItems)==0:
                    if checkFrequency<len(checkFrequencies)-1 and lastReadWasBlank:
                        checkFrequency+=1
                        lastReadWasBlank=0
                        print "Nothing this iteration. Dropping check frequency to",checkFrequencies[checkFrequency],"seconds."
                    lastReadWasBlank=1
                time.sleep(checkFrequencies[checkFrequency])
            except Exception as detail:
                print "RSS Grabbing failure! Bad feed?"
                time.sleep(180)

        for channel in channels:
            Queue.put("#PRIVMSG "+channel+" :MetConst Reader "+name+" Shut down.\r\n")
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]
