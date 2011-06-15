# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        names=globalv.channelUsers[complete.channel()][:]
        random.shuffle(names)
        return ["PRIVMSG $C$ :"+names[0]]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
