# -*- coding: utf-8 -*-
from plugins import plugin
from securityHandler import isAllowed
from userlevelHandler import getLevel
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
        channel=complete.channel()
        sender=complete.userMask()
        if isAllowed(sender)>=getLevel(complete.cmd()[0]):
            if msg!="":
                chan=msg
                if chan[0]!="#":
                    chan="#"+chan
                msg="PART "+chan
                try:
                    globalv.channels.remove(chan)
                except:
                    pass
            else:
                msg="PART "+channel
            return [msg]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
