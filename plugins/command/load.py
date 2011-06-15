# -*- coding: utf-8 -*-
from plugins import plugin
from settingsHandler import readSetting
from pluginHandler import load_plugin, unload_plugin
from aliasHandler import load_alias
from securityHandler import isAllowed
from userlevelHandler import getLevel
import globalv
import sys
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 50
    def action(self, complete):
        name=complete.message().split()[0]
        loadAs=""
        if len(complete.message().split())==3:
            loadAs = complete.message().split()[2]
        loadBlacklist=["special"]
        if name.lower() in loadBlacklist and isAllowed(complete.userMask())<150:
            return ["PRIVMSG $C$ :Owner only plugin!"]
        if isAllowed(complete.userMask())<getLevel(complete.cmd()[0]):
            return ["PRIVMSG $C$ :Sorry, only elevated users can load plugins!"]
        if name in globalv.loadedAliases.keys():
            try:
                extension=globalv.loadedAliases[name]
                unload_plugin(name)
                pluginName=extension.split()[0]
                x=__import__(pluginName)
                reload(x)
                globalv.loadedPlugins[pluginName]=x.pluginClass()
                load_alias(name, extension)
                msg="Reloaded alias "+name+" successfully!"
            except Exception as detail:
                msg="Load failure: "+str(detail)
        else:
            try:
                state=load_plugin(name, loadAs)
                msg="oaded "+name+" successfully!"
                msg="L"+msg if state==0 else "Rel"+msg
            except Exception as detail:
                msg="Load failure: "+str(detail)
        if complete.message().split()[1:]==["silently"]:
            return [""]
        else:
            return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !load module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!load [plugin]"]
