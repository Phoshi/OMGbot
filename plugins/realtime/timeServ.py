# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from time import time as currentTime
class pluginClass(plugin):
    def gettype(self):
        return "special"
    def action(self, complete):
        if complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="TIME":
            time=' '.join(complete.message().split())[:-1]
            if complete.user() in globalv.timeUsers.keys():
                channel=globalv.timeUsers[complete.user()]
            else:
                channel="PY"
            return ["PRIVMSG "+channel+" :"+complete.user()+"'s local time is: "+time]
        elif complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="\001VERSION":
            time=' '.join(complete.message().split())[:-1]
            if complete.user() in globalv.timeUsers.keys():
                channel=globalv.timeUsers[complete.user()]
            else:
                channel="PY"
            return ["PRIVMSG "+channel+" :"+complete.user()+"'s version is: "+time]
        elif complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="\001FINGER":
            time=' '.join(complete.message().split())[:-1]
            if complete.user() in globalv.timeUsers.keys():
                channel=globalv.timeUsers[complete.user()]
            else:
                channel="PY"
            return ["PRIVMSG "+channel+" :"+complete.user()+"'s finger is: "+time]
        elif complete.type()=="NOTICE" and complete.fullMessage().split()[0]=="\001PING":
            now=currentTime()
            then=float(complete.message()[:-1])
            if complete.user() in globalv.timeUsers.keys():
                channel=globalv.timeUsers[complete.user()]
            else:
                channel="PY"
            return ["PRIVMSG "+channel+" :Received %s's pong in %s seconds."%(complete.user(), (now-then))]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
