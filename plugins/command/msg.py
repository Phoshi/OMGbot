# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=' '.join(complete.message().split()[1:])
        user=complete.message().split()[0].lower()
        yeahNo=["chanserv","nickserv","memoserv"]
        if user not in yeahNo:
            return ["PRIVMSG "+user+" :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
