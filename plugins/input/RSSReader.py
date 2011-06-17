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
        colour="\x03"
        self.Queue.put("#PRIVMSG %s :RSS Reader started up successfully\r\n"%(channel))
        feeds = []
        feedNames = {}
        latestFeedItem = {}
        checkFrequencies=[10,20,30,60,120,180,240,300]
        lastReadWasBlank=0
        checkFrequency=0
        while running:
            print "Looping!"
            while not inputQueue.empty():
                data = inputQueue.get()
                print "Data in queue:",data
                if data=="stop":
                    running = False
                    break
                if data.split()[0]=="add":
                    feeds.append(data.split()[1])
                    potentialName = ' '.join(data.split()[2:])
                    print data.split()[1]
                    if potentialName.strip()=="":
                        potentialName = data.split()[1]
                    print potentialName
                    feedNames[data.split()[1]] = potentialName
                    latestFeedItem[data.split()[1]]=""
                    Queue.put("#PRIVMSG %s :Added feed to list!\r\n"%channel)
                if data.split()[0]=="remove":
                    if data.split()[1] in feeds:
                        feeds.remove(data.split()[1])
                        Queue.put("#PRIVMSG %s :Removed feed from list!\r\n"%channel)
                    else:
                        Queue.put("#PRIVMSG %s :Feed not currently being read!\r\n"%channel)
                if data.split()[0]=="intervals":
                    checkFrequencies = [int(checkTime) for checkTime in data.split()[1:]]
                    checkFrequency = 0
                    Queue.put("#PRIVMSG %s :Set check intervals\r\n"%channel)
                if data.split()[0]=="list":
                    Queue.put("#PRIVMSG %s :RSS Reader for channel %s is following:\r\n"%(channel, channel))
                    for feed in feeds:
                        Queue.put("#PRIVMSG %s :%s: %s\r\n"%(channel, feedNames[feed], feed))

                    
            try:
                for feedName in feeds:
                    feed=feedparser.parse("http://"+feedName)
                    newFeedItem=feed.entries[0].id
                    newItems=[]
                    if newFeedItem!=latestFeedItem[feedName]:
                        iterateBack=0
                        while (feed.entries[iterateBack].id!=latestFeedItem[feedName] and iterateBack<len(feed.entries)-1 and iterateBack < 5):
                            newItems.append ((feed.entries[iterateBack].link, feed.entries[iterateBack].title))
                            iterateBack+=1
                        latestFeedItem[feedName]=newFeedItem
                        for item in newItems:
                            Queue.put("#PRIVMSG "+channel+" :\x0312"+feedNames[feedName]+"\x03:\x0311 "+item[1]+"\x03 (at \x0312"+(item[0] if len(item[0])<20 else bitly(item[0]))+"\x03)\r\n")
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
