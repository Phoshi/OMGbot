# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __append_seperator__(self):
        return True
    def action(self, complete):
        msg=complete.message().split('::')[0]
        if msg.split()[0][0]=="-" and msg.split()[0][1:].isdigit():
            numMatches=int(msg.split()[0][1:])
            msg=' '.join(msg.split()[1:])
        else:
            numMatches=99
        match=re.findall(msg,complete.message().split('::')[1])
        print match
        if len(match)>0:
            match=', '.join(match[:numMatches])
        else:
            match="No Matches"
        return ["PRIVMSG $C$ :"+match]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
