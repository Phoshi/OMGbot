# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from time import strftime
class pluginClass(plugin):
    def gettype(self):
        return "preprocess"
    def action(self, complete):
        if complete.type()=="PING":
            pass
        elif complete.type()=="PRIVMSG" or complete.type()=="NOTICE":
            print strftime("[%H:%M]"),complete.channel()+": <"+complete.user()+">",complete.fullMessage()
        else:
            print strftime("[%H:%M]"),complete.complete()
        return complete.complete()
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the shows all input in the bot's terminal.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None."]
