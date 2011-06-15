# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
import shlex
import braceParser
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
    def action(self, complete):
        reload(braceParser)
        parseBraces=braceParser.parseBraces
        try:
            msg=parseBraces(complete.fullMessage())
        except Exception as detail:
            return ["PRIVMSG $C$ :Parse Failure: "+str(detail)]
        conditionState=True
        toReturn=[]
        for condition in msg[0]:
            try:
                calcInput=":%s PRIVMSG %s :!%s %s"%(complete.userMask(),complete.channel(),"calculate", condition)
                inputObj=formatInput(pluginArguments(calcInput))
                output=':'.join(globalv.loadedPlugins["calculate"].action(inputObj)[0].split(':')[1:])
                if output=="False":
                    conditionState=False
                    break
            except Exception as detail:
                return ["PRIVMSG $C$ :Conditional execution failure in %s"%condition,"PRIVMSG $C$ :Reason:%s"%str(detail)]

        if conditionState==True:
            commandList=msg[1][0].split(';')
        elif len(msg[1])>1:
            commandList=msg[1][1].split(';')
        else:
            commandList=[]
        for command in commandList:
            try:
                plugin=command.split()[0]
                args=' '.join(command.split()[1:])
                input=":%s PRIVMSG %s :!%s %s"%(complete.userMask(),complete.channel(),plugin, args)
                inputObj=formatInput(pluginArguments(input))
                toReturn+=[x.replace('\x00','').encode('utf-8') for x in globalv.loadedPlugins[plugin.split()[0]].action(inputObj)]
            except Exception as detail:
                return ["PRIVMSG $C$ :!if failure in command %s"%command,"PRIVMSG $C$ :Reason:%s"%str(detail)]
        return toReturn 
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !kick module","PRIVMSG $C$ :Usage: (Requires Elevated Bot Privileges)","PRIVMSG $C$ :!kick [user]"]
