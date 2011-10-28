# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import shlex
import re
from pluginArguments import pluginArguments
from pluginFormatter import formatInput, formatOutput

class pluginClass(plugin):
    def gettype(self):
        return "command"
    def expand(self, toExpand, toExpandWith):
        expansions = re.findall("\$([0-9]*)\$", toExpand)
        if len(expansions) == 0 and toExpand.find('$*$')==-1:
            return "%s%s"%(toExpand, toExpandWith)
        for expansion in expansions:
            index = int(expansion)-1
            if len(toExpandWith.split())>index:
                toExpand = toExpand.replace("$%s$"%expansion, toExpandWith.split()[index])
        toExpand = toExpand.replace('$*$', toExpandWith)
        return toExpand


    def action(self, complete):
        commands = shlex.split(complete.message())
        commands = [c.replace("\x00","") for c in commands] #Working around a unicode bug in shlex
        commandString = commands[0]
        commands = commands[1:15]
        commandString = commandString.split(' ',1)
        outputList=[]
        for command in commands:
            if len(commandString)>1:
                argumentsToRun = self.expand(commandString[1], command)
            else:
                argumentsToRun = command 
            commandToRun = commandString[0]
            print "Running command", commandToRun, "with arguments", argumentsToRun
            print "Constructing plugin object"
            arguments = pluginArguments(complete.complete())
            firstBit=arguments.complete().split(':')[1]
            arguments.setComplete(":"+firstBit+":"+globalv.commandCharacter+commandToRun+" "+argumentsToRun)
            print "Pre-formatting plugin object:", arguments.complete()
            arguments=formatInput(arguments)
            print "Running command"
            pluginOutput=globalv.loadedPlugins[commandToRun].action(arguments)
            print "Formatting output"
            output = formatOutput(pluginOutput, complete)
            print "Decoding output"
            output = [o for o in output]
            print "Success! Adding output to output list",output
            outputList+=output
        return outputList
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
