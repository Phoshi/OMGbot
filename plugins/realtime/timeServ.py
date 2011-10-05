# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from time import time as currentTime
class pluginClass(plugin):
    def gettype(self):
        return "special"
    
    def getChannel(self, user):
        user = user.lower()
        for u in globalv.timeUsers:
            if u.lower() == user:
                return globalv.timeUsers[u]
        return "PY"
    
    def action(self, complete):
        if complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="TIME":
            time=' '.join(complete.message().split())[:-1]
            channel=self.getChannel(complete.user())
            return ["PRIVMSG "+channel+" :"+complete.user()+"'s local time is: "+time]
        elif complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="\001VERSION":
            time=' '.join(complete.message().split())[:-1]
            channel=self.getChannel(complete.user())
            return ["PRIVMSG "+channel+" :"+complete.user()+"'s version is: "+time]
        elif complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="\001FINGER":
            time=' '.join(complete.message().split())[:-1]
            channel=self.getChannel(complete.user())
            return ["PRIVMSG "+channel+" :"+complete.user()+"'s finger is: "+time]
        elif complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="\001PING":
            now=currentTime()
            then=float(complete.message()[:-1])
            channel=self.getChannel(complete.user())
            return ["PRIVMSG "+channel+" :Received %s's pong in %s seconds."%(complete.user(), (now-then))]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
