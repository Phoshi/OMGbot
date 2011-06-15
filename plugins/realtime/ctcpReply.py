# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def action(self, complete):
        if complete.type()=="PRIVMSG" and complete.channel()[0]!="#":
            if complete.fullMessage()=="\001TIME\001":
                timeString=time.strftime("%H:%M - %d/%m/%Y")
                return ["NOTICE $C$ :\001TIME "+timeString+"\001"]
            elif complete.fullMessage()=="\001VERSION\001":
                return ["NOTICE $C$ :\001VERSION OMGbot version 2\001"]
            elif complete.fullMessage()=="\001SOURCE\001":
                return ["NOTICE $C$ :\001SOURCE Run !source OMGbot to grab the latest source, or !source [plugin] for a plugin source\001"]
            elif complete.fullMessage()=="\001CLIENTINFO\001":
                return ["NOTICE $C$ :\001CLIENTINFO VERSION, SOURCE, CLIENTINFO, PING\001"]
            elif complete.fullMessage().split()[0]=="\001PING":
                return ["NOTICE $C$ :"+complete.fullMessage()]
            elif complete.fullMessage()=="\001PING\001":
                return ["NOTICE $C$ :\001PING PONG\001"]
            elif complete.fullMessage()=="\001FINGER\001":
                return ["NOTICE $C$ :\001FINGER OMGbot - Idle Time: 0 seconds. I do not sleep.\001"]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
