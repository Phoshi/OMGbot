# -*- coding: utf-8 -*-
from plugins import plugin
from settingsHandler import readSetting
from pluginHandler import load_plugin, unload_plugin
from aliasHandler import load_alias
from securityHandler import isAllowed
from userlevelHandler import getLevel
import globalv
import settingsHandler
import sys
import shlex
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 200
    def action(self, complete):
        name=complete.message().split()[0]
        if len(complete.message().split())>1:
            noKill=1
        else:
            noKill=0
        msg="Successfully asked the plugin to stop"
        if isAllowed(complete.userMask())<getLevel(complete.cmd()[0]):
            return ["PRIVMSG $C$ :Only elevated users can do that!"]
        try:
            globalv.loadedInputs[name.split()[0]].put("stop")
            del globalv.loadedInputs[name.split()[0]]
            if not noKill:
                settingsHandler.deleteSetting("'core-input'","input",name)
        except Exception as detail:
            msg="Unload failure: "+str(detail)
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !addInput module!","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!addInput [name] [plugin name] [arguments to plugin]"]
