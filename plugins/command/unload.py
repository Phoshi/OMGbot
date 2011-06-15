# -*- coding: utf-8 -*-
from plugins import plugin
from settingsHandler import readSetting
from pluginHandler import unload_plugin
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
        name=msg.split()[0]
        if isAllowed(complete.userMask())<getLevel(complete.cmd()[0]):
            return ["PRIVMSG $C$ :Sorry, only elevated users can do that!"]
        if name=="load" and complete[0].split()[0].split('!')[0]!=readSetting("core","username"):
            return ["PRIVMSG $C$ :Silly bugger, that would break the world!"]
        success=unload_plugin(name)
        if name in globalv.loadedAliases.keys():
            del globalv.loadedAliases[name]
        if msg.split()[1:]==['silently']:
            return [""]
        if success:
            return ["PRIVMSG $C$ :Unload successful!"]
        else:
            return ["PRIVMSG $C$ :Plugin is not loaded!"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
