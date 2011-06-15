# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
from pluginArguments import pluginArguments
from pluginFormatter import formatOutput, formatInput
import time
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def action(self, complete):
        user=complete.user()
        if complete.type()=="JOIN":
            globalv.channelUsers[complete.channel()].append(complete.user())
        elif complete.type()=="PART":
            globalv.channelUsers[complete.channel()].remove(complete.user())
        elif complete.type()=="QUIT":
            for channel in globalv.channelUsers.keys():
                if complete.user() in globalv.channelUsers[channel]:
                    globalv.channelUsers[channel].remove(complete.user())
        elif complete.type()=="KICK":
            globalv.channelUsers[complete.channel()].remove(complete.complete()[1:].split()[3])
        elif complete.complete().split()[1]=="NICK":
            for channel in globalv.channelUsers.keys():
                if complete.user() in globalv.channelUsers[channel]:
                    globalv.channelUsers[channel].remove(complete.user())
                    globalv.channelUsers[channel].append(complete.fullMessage())
        elif complete.type()=="353":
            message=complete.complete()
            channel=message.split()[4]
            names=message[1:].split(':')[1].split()
            names=[name[1:] if name[0] in ["+","@","%"] else name for name in names]
            globalv.channelUsers[channel]=names
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
