# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 50
    def action(self, complete):
        msg=complete.message()
        sender=complete.channel()
        globalv.variables['lasttopic']=globalv.miscVars[4][complete.channel()][0]
        if isAllowed(complete.userMask())<getLevel(complete.cmd()[0]) and len(msg)!=0:
            return [""]
        if msg=="":
            return ["PRIVMSG $C$ :"+' '.join(globalv.miscVars[4][sender])]
        if msg.split()[0]=="add":
            return ["TOPIC $C$ :"+' '.join(globalv.miscVars[4][sender])+" | "+' '.join(msg.split()[1:])]
        elif msg.split()[0]=="remove":
            return ["TOPIC $C$ :"+' | '.join(' '.join(globalv.miscVars[4][sender]).split(' | ')[:-int(msg.split()[1])])]
        else:
            return["TOPIC $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !topic module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!topic [OPTIONAL add/remove] [text/number of sections to remove]"]
