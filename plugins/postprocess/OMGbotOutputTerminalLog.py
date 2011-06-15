# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
class pluginClass(plugin):
    def gettype(self):
        return "postprocess"
    def action(self, complete):
        if complete.split()[0]=="PONG":
            return complete
        msg=complete.split()
        if len(msg)>1:
            if msg[0]=="PRIVMSG":
                print time.strftime("[%H:%M]"),msg[1]+":", "<OMGbot>", ' '.join(msg[2:])[1:]
            else:
                print time.strftime("[%H:%M]"), complete
        return complete
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the plugin that shows output loggery in the bot's terminal.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None."]
