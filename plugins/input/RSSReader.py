# -*- coding: utf-8 -*-
from plugins import plugin
from bitlyServ import bitly
import time
import feedparser
import globalv
import traceback
class asyncInput(object):
    def __init__(self,Queue, inputQueue, channel):
        self.Queue=Queue
        running = True
        initComplete = False #To silence input before startup is handled
        colour="\x03"
        self.Queue.put("#PRIVMSG %s :RSS Reader started up successfully\r\n"%(channel))
        feeds = []
        feedNames = {}
        latestFeedItem = {}
        checkFrequencies=[10,20,30,60,120,180,240,300]
        lastReadWasBlank=0
        checkFrequency=0
        while running:
            while not inputQueue.empty():
                data = inputQueue.get()
                if data=="stop":
                    running = False
                    break
                if data.split()[0]=="add":
                    feedLink = data.split()[1]
                    if feedLink[:7]=="http://":
                        feedLink = feedLink[7:]
                    feeds.append(feedLink)
                    potentialName = ' '.join(data.split()[2:])
                    if potentialName.strip()=="":
                        potentialName = feedLink
                    feedNames[feedLink] = potentialName
                    feed=feedparser.parse("http://"+feedLink)
                    if (len(feed.entries) == 0):
                        continue
                    latestFeedItem[feedLink]=feed.entries[0].id
                    if initComplete:
                        Queue.put("#PRIVMSG %s :Added feed to list!\r\n"%channel)
                if data.split()[0]=="remove":
                    if data.split()[1] in feeds:
                        feeds.remove(data.split()[1])
                        if initComplete:
                            Queue.put("#PRIVMSG %s :Removed feed from list!\r\n"%channel)
                    else:
                        if initComplete:
                            Queue.put("#PRIVMSG %s :Feed not currently being read!\r\n"%channel)
                if data.split()[0]=="intervals":
                    checkFrequencies = [int(checkTime) for checkTime in data.split()[1:]]
                    checkFrequency = 0
                    if initComplete:
                        Queue.put("#PRIVMSG %s :Set check intervals\r\n"%channel)
                if data.split()[0]=="list":
                    if initComplete:
                        Queue.put("#PRIVMSG %s :RSS Reader for channel %s is following:\r\n"%(channel, channel))
                        for feed in feeds:
                            Queue.put("#PRIVMSG %s :%s: %s\r\n"%(channel, feedNames[feed], feed))
                if data=="--init--":
                    initComplete = True

                    
            try:
                for feedName in feeds:
                    feed=feedparser.parse("http://"+feedName)
                    if (len(feed.entries) == 0):
                        continue
                    newFeedItem=feed.entries[0].id
                    newItems=[]
                    if newFeedItem!=latestFeedItem[feedName]:
                        iterateBack=0
                        while (feed.entries[iterateBack].id!=latestFeedItem[feedName] and iterateBack<len(feed.entries)-1 and iterateBack < 5):
                            newItems.append ((feed.entries[iterateBack].link, feed.entries[iterateBack].title))
                            iterateBack+=1
                        latestFeedItem[feedName]=newFeedItem
                        for item in newItems:
                            Queue.put("#PRIVMSG "+channel+" :\x02"+feedNames[feedName]+"\x02: "+item[1]+" (at \x02"+(item[0] if len(item[0])<20 else bitly(item[0]))+"\x02)\r\n")
                        if checkFrequency>0:
                            checkFrequency-=len(newItems)
                            checkFrequency=0 if checkFrequency<0 else checkFrequency
                        
                    if len(newItems)==0:
                        if checkFrequency<len(checkFrequencies)-1 and lastReadWasBlank:
                            checkFrequency+=1
                            lastReadWasBlank=0
                        lastReadWasBlank=1
            except Exception as detail:
                print "RSS Grabbing failure! Bad feed?"
                print detail
                traceback.print_exc()
                time.sleep(60)
            time.sleep(checkFrequencies[checkFrequency])
        Queue.put("#PRIVMSG "+channel+" :RSS Reader shut down.\r\n")
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I watch RSS feeds and talk about new entries!"]
