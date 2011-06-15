# -*- coding: utf-8 -*-
from plugins import plugin
from securityHandler import isAllowed
from userlevelHandler import getLevel
import re
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            if msg in globalv.miscVars[0].keys():
                msg=globalv.miscVars[0][msg]
            return ['MODE $C$ -b '+msg]
        else:
            return [""]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !unban module. I un-banish people.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!unban [user] (Hostmasks are stored locally)"]
