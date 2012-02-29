# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from random import gauss
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        input = [int(x) for x in complete.message().split()]
        return ["PRIVMSG $C$ :"+str(int(gauss(input[0], input[1])))]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
