# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
from pluginFormatter import formatInput
from pluginArguments import pluginArguments
from userlevelHandler import getLevel
from securityHandler import isAllowed
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init__(self):
        self.Voted={}
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "votes","plugin")
        settingsHandler.writeSetting(name,["votes","plugin"],["3","9"])
    def action(self, complete):
        msg=complete.message()
        votes=int(settingsHandler.readSetting(complete.cmd()[0], "votes"))
        plugin=settingsHandler.readSetting(complete.cmd()[0], "plugin")
        user=complete.userMask().split('!')[1]
        if msg.lower() in self.Voted.keys():
            if user in self.Voted[msg.lower()]:
                return ["PRIVMSG $C$ :You have already voted!"]
            else:
                self.Voted[msg.lower()].append(user)
                numRequired=votes-len(self.Voted[msg.lower()])
                if numRequired>0:
                    if msg!="":
                        msg=" "+msg
                    if numRequired!=1:
                        s="s"
                    else:
                        s=""
                    return ["PRIVMSG $C$ :Voted to %s%s. %s more vote%s required."%(plugin,msg,numRequired,s)]
        else:
            self.Voted[msg.lower()]=[user]
            numRequired=votes-len(self.Voted[msg.lower()])
            if msg!="":
                msg=" "+msg
            if numRequired!=1:
                s="s"
            else:
                s=""
            return ["PRIVMSG $C$ :Voted to %s%s. %s more vote%s required."%(plugin,msg,numRequired,s)]
        if len(self.Voted[msg.lower()])>=votes:
            input=":%s!%s PRIVMSG %s :!%s %s"%(globalv.nickname,globalv.miscVars[0][globalv.nickname],complete.channel(),plugin, msg)
            inputObj=formatInput(pluginArguments(input))
            output=globalv.loadedPlugins[plugin.split()[0]].action(inputObj)
            self.Voted[msg.lower()]=[]
            return output
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !kick module","PRIVMSG $C$ :Usage: (Requires Elevated Bot Privileges)","PRIVMSG $C$ :!kick [user]"]
