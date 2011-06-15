# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
from securityHandler import isAllowed
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        if isAllowed(complete.userMask())<1:
            return [""]
        MCName=complete.message().split()[0]
        IRCName=complete.user()
        settingsHandler.writeSetting("stripMCBotNames", ["minecraft", "irc"], [MCName, IRCName])
        return ["PRIVMSG $C$ :Names linked - please reload stripMCBotNames for the changes to take effect"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
