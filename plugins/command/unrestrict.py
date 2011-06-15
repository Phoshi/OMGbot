# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
        nick=complete.userMask()
        if isAllowed(nick)>=getLevel(complete.cmd()[0]):
            if msg.split()[1] in globalv.accessRights[msg.split()[0]]:
                globalv.accessRights[msg.split()[0]].remove(msg.split()[1])
                msg="Ok, removed that restriction."
            else:
                msg="That user can already use that command!"
        else:
            msg="Sorry, only administrators can use this command!"
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
