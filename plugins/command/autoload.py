# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from userlevelHandler import getLevel
import os
from securityHandler import isAllowed
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def action(self, complete):
        msg=complete.message()
        sender=complete.userMask()
        if len(msg.split())>1:
            mode=msg.split()[1].lower()
        else:
            mode="on"
        msg=msg.split()[0]
        print sender
        print globalv.basePlugin
        if msg=="list":
            return ["PRIVMSG $C$ :"+', '.join([x[0] for x in settingsHandler.readSettingRaw("coreAutoLoad", "loadAs")])]
        if isAllowed(sender)>=getLevel(complete.cmd()[0]):
            if mode=="on":
                settingsHandler.writeSetting("coreAutoLoad", ["plugin", "loadAs"], [globalv.basePlugin[msg], msg])
                return ["PRIVMSG $C$ :Plugin set to autoload"]
            else:
                settingsHandler.deleteSetting("coreAutoLoad", "loadAs", msg)
        return ["PRIVMSG $C$ :You do not have the required access rights!"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !autoload module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!autoload [plugin] [on/off]"]
