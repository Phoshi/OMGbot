# -*- coding: utf-8 -*-
from plugins import plugin
from userlevelHandler import getLevel
from securityHandler import isAllowed
import globalv
import os
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "location")
        settingsHandler.writeSetting(name, "location","/home/py/")
    def action(self, complete):
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            url=complete.message()
            location=settingsHandler.readSetting(complete.cmd()[0],"location")
            wgetString="wget -N --directory-prefix=%s %s &"%(location, url)
            print wgetString
            os.system(wgetString)
            return ["PRIVMSG $C$ :Downloading %s to %s."%(url, location)]
        else:
            return ["PRIVMSG $C$ :Sorry, you need higher priviledges to download files!"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
