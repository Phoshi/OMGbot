# -*- coding: utf-8 -*-
from plugins import plugin
from pluginArguments import pluginArguments
from pluginFormatter import formatInput, formatOutput
import globalv
import random
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        commands=msg.split('|')
        random.shuffle(commands)
        command=commands[0]
        plugin=command.split()[0]
        arguments=' '.join(command.split()[1:])
        arguments=":%s PRIVMSG %s :!%s %s"%(complete.userMask(), complete.channel(),plugin ,arguments)
        arguments=formatInput(pluginArguments(arguments))
        pluginOutput=globalv.loadedPlugins[plugin].action(arguments)
        return pluginOutput 
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]

