# -*- coding: utf-8 -*-
from plugins import plugin
from aliasHandler import rename_alias
from pluginHandler import rename_plugin
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
        print globalv.basePlugin
        if (isAllowed(complete.userMask()) < getLevel(complete.cmd()[0])):
            return ["PRIVMSG $C$ :You do not have the neccesary access rights to perform this operation"]
        if (msg.split()[0] in globalv.loadedAliases.keys()):
            if (len(msg.split()) == 2):
                result = rename_alias(msg.split()[0], msg.split()[1])
                if (result):
                    return ["PRIVMSG $C$ :Alias renamed!"]
                else:
                    return ["PRIVMSG $C$ :Alias could not be renamed!"]
        else:
            if (len(msg.split()) == 2):
                result = rename_plugin(msg.split()[0], msg.split()[1])
                if (result):
                    return ["PRIVMSG $C$ :Command renamed!"]
                else:
                    return ["PRIVMSG $C$ :Command could not be renamed!"]
        return ["PRIVMSG $C$ :Invalid arguments"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !alias module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!alias [what] [plugin] [arguments]"]
