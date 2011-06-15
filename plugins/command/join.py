# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def action(self, complete):
        msg=complete.message()
        sender=complete.userMask()
        if isAllowed(sender)>=getLevel(complete.cmd()[0]):
            if msg!="":
                chan=msg
                if chan[0]!="#":
                    chan="#"+chan
                msg="JOIN "+chan
                globalv.channels.append(chan)
                return [msg]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !join module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!join #channel"]
