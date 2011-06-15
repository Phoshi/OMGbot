# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import re
import htmlentitydefs
class pluginClass(plugin):
    def gettype(self):
        return "postprocess"
    def action(self, complete):
        return complete.replace('\n',' ').replace('\r', ' ')
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the plugin that shows output loggery in the bot's terminal.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None."]
