# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from securityHandler import isAllowed
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        hostmask = globalv.miscVars[0][complete.message()]
        return ["PRIVMSG $C$ :"+str(isAllowed(hostmask))]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
