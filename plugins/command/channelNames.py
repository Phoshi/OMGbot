# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        print globalv.channelUsers
        names=['"%s"'%name for name in globalv.channelUsers[complete.channel()]]
        return ["PRIVMSG $C$ :[%s]"%', '.join(names)]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
