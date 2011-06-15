# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        if len(globalv.outputQueue) > 0:
            message = globalv.outputQueue.pop(0)
        else:
            message = "PRIVMSG $C$ :No items in queue."
        return message.decode('utf-8')
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
