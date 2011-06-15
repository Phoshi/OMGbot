# -*- coding: utf-8 -*-
from plugins import plugin
import globalv,sys,os
from pluginHandler import load_plugin, unload_plugin
from aliasHandler import load_alias
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        for line in settingsHandler.readSetting("alias","aliasName, aliasPlugin, aliasArguments"):
            load_alias(line[0], ' '.join(line[1:]))

        return ["PRIVMSG $C$ :Ok, done."]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
