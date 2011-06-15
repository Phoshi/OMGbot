# -*- coding: utf-8 -*-
from plugins import plugin
from settingsHandler import readSetting
from userlevelHandler import getLevel
from securityHandler import isAllowed
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 200
    def action(self, complete):
        msg=complete.message()
        sender=complete.user()
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            globalv.miscVars[2].append(msg)
            import random
            msg="LOWERING SHIELDS TO "+str(random.randint(0,100))+"%"
            return ["PRIVMSG $C$ :"+msg]
        else:
            return ["PRIVMSG $C$ :Don't be silly, only administrators can do that, $U$."]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
