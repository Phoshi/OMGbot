# -*- coding: utf-8 -*-
from plugins import plugin
from securityHandler import isAllowed
from userlevelHandler import getLevel
import globalv
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def action(self, complete):
        msg=complete.message()
        blacklist=["quit","part","join","kick","nick","mode"]
        nick=complete.userMask()
        if isAllowed(nick)<getLevel(complete.cmd()[0]):
            return [""] 
        return [msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !special module","PRIVMSG $C$ :Usage: (Requires Elevated Bot Privileges)","PRIVMSG $C$ :!special [raw string]"]
