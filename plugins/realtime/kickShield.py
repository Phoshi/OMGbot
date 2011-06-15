# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "special"
    def action(self, complete):
        if complete.type()=="MODE":
            if complete.complete().find("+b")!=-1:
                return ["PRIVMSG CHANSERV :UNBAN $C$"]
        if complete.type()=="KICK" and complete.complete()[1:].split()[3]==globalv.nickname:
            return ["PRIVMSG CHANSERV :UNBAN $C$","JOIN $C$"]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
