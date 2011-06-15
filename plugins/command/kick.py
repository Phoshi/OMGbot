# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
from userlevelHandler import getLevel
from securityHandler import isAllowed
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            kickMessage=' '.join(msg.split()[1:])
            if kickMessage=="":
                kickMessage="Go away."
            toKick=["KICK $C$ "+msg.split()[0]+" :"+kickMessage]
            return toKick
        else:
            kickMessage=' '.join(msg.split()[1:])
            if kickMessage=="":
                kickMessage="Go away."
            return ["PRIVMSG $C$ :ACTION kicks "+msg.split()[0]+" in the shin (%s)"%kickMessage]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !kick module","PRIVMSG $C$ :Usage: (Requires Elevated Bot Privileges)","PRIVMSG $C$ :!kick [user]"]
