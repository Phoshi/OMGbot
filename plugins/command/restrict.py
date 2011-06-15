# -*- coding: utf-8 -*-
from plugins import plugin
from securityHandler import isAllowed
from userlevelHandler import getLevel
import globalv,re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 50
    def action(self, complete):
        msg=complete.message()
        nick=complete.userMask()
        sender=complete.channel()
        if msg.split()[1] in globalv.loadedPlugins.keys():
            if isAllowed(nick)>=getLevel(complete.cmd()[0]):
                if msg.split()[1]=="unrestrict":
                    return ["PRIVMSG $C$ :Don't be silly."]
                globalv.accessRights[msg.split()[0]].append(msg.split()[1])
                msg="Ok, restricted that command for that user."
            else:
                msg="Sorry, only administrators can use this command!"
        else:
            msg="Plugin would not appear to exist"
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !restrict module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!restrict [user] [command]"]
