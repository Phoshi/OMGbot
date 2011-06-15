# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from userlevelHandler import getLevel
from securityHandler import isAllowed
import re
import settingsHandler
class pluginClass(plugin):
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "kickAfterBan")
        settingsHandler.writeSetting(name, "kickAfterBan", "False")
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message().split()[0]
        kickReason=' '.join(complete.message().split()[1:])
        if kickReason=="":
            kickReason="Go Away."
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            if msg in globalv.miscVars[0].keys():
                hostmask=globalv.miscVars[0][msg]
            print hostmask
            toReturn=['MODE $C$ +b '+hostmask]
            if settingsHandler.readSetting(complete.cmd()[0], "kickAfterBan")=="True":
                toReturn.append("KICK $C$ "+msg+" :"+kickReason)
            return toReturn
        else:
            print "ID failure:",msg,"not in",globalv.miscVars[0][msg]
            return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !ban module. I banish people.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!ban [user] (hostmasks stored locally)"]
