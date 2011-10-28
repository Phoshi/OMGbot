# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
import urllib2
import json

class Stream(object):
    Name = ""
    Channel = ""
    Thread = ""

    isLive = False

    def __init__(self, channel, artist, thread):
        self.Name = artist
        self.Channel = channel
        self.Thread = thread


    def getChannel(self):
        return "http://www.livestream.com/%s"%self.Channel
    def getName(self):
        if self.Name=="":
            return self.Channel
        return self.Name
    def getThread(self):
        return Thread

    def updateStatus(self):
        print "Checking status for",self.Channel
        statusFeed = "http://x" + self.Channel + "x.api.channel.livestream.com/2.0/livestatus.json"
        text = urllib2.urlopen(statusFeed).read()
        statusDict = json.loads(text)
        self.isLive = statusDict["channel"]["isLive"]
    def status(self):
        self.updateStatus()
        return self.isLive


class asyncInput(object):
    def __init__(self,Queue, inputQueue, outputChannel):
        running = True
        self.Queue=Queue
        streams = []
        try:
            drawfriendsUrl = "http://www.fimfiction.net/drawfriendstreams/streams.txt"
        except:
            Queue.put("#PRIVMSG %s :Cannot access drawfriend streams list at http://www.fimfiction.net/drawfriendstreams/streams.txt\r\n"%outputChannel)
            return
        drawfriendsText = urllib2.urlopen(drawfriendsUrl).read()
        drawfriendsDict = json.loads(drawfriendsText)
        streamsDict = drawfriendsDict["streams"]

        streams = []

        for stream in streamsDict:
            channel = stream["channel"]
            artist = stream["artist"]
            if "thread" in stream.keys():
                thread = stream["thread"]
            else:
                thread = ""

            newStream = Stream(channel, artist, thread)
            streams.append(newStream)


        globalv.variables["drawfriendStreams"] = streams
        print "Sending success message to",outputChannel
        Queue.put("#PRIVMSG %s :Drawfriend Stream Notifier started successfully!\r\n"%outputChannel)
        while running:
            while not inputQueue.empty():
                data = inputQueue.get()
                if data=="stop":
                    running = False
                    break

            for stream in streams:
                oldStatus = stream.isLive
                try:
                    newStatus = stream.status()
                except:
                    print "DrawFriends Updater: Could not update",stream.getName()+"'s", "stream!"
                    continue
                if oldStatus != newStatus:
                    message = "%s %s streaming: \x02%s\r\n"%(stream.getName(), "started" if newStatus else "stopped", stream.getChannel())
                    Queue.put("#PRIVMSG %s :%s"%(outputChannel, message))

            time.sleep(60 * 10)
        Queue.put("#PRIVMSG %s :Drawfriend stream reader shutting down!\r\n"%outputChannel)
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I SAY X EVERY Y"]
