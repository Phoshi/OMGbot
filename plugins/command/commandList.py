# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
from pluginFormatter import formatInput
from pluginArguments import pluginArguments
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init_db_tables__(self, name):
        if settingsHandler.tableExists("'"+name+"'")==False:
            settingsHandler.newTable("'"+name+"'","answer")
    def __init_answers__(self, complete,beRandom):
        self.answers=[x[0] for x in settingsHandler.readSetting("'"+complete.cmd()[0]+"'","answer")]
        if beRandom:
            random.shuffle(self.answers)
    def __level__(self):
        return 0
    def __init__(self):
        self.answers=[]
    def action(self, complete):
        msg=complete.message()
        isElevated=(isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]))
        beRandom=True
        if len(self.answers)==0:
            self.__init_answers__(complete,beRandom)
        if len(msg.split())>=1:
            cmd=msg.split()[0]
            msg=' '.join(msg.split()[1:])
        else:
            cmd=""
            msg=""
        if cmd=="-add" and isElevated:
            settingsHandler.writeSetting("'"+complete.cmd()[0]+"'","answer",msg)
            toReturn="Added that answer"
            self.__init_answers__(complete,beRandom)
        elif cmd=="-delete" and isElevated:
            settingsHandler.deleteSetting("'"+complete.cmd()[0]+"'","answer",msg)
            toReturn="Wiped that answer."
            self.__init_answers__(complete,beRandom)
        elif cmd=="-wipe" and isElevated:
            settingsHandler.dropTable("'"+complete.cmd()[0]+"'")
            settingsHandler.newTable("'"+complete.cmd()[0]+"'","answer")
            toReturn="Answer table wiped!"
            self.__init_answers__(complete,beRandom)
        elif cmd=="-reset" and isElevated:
            self.__init_answers__(complete,beRandom)
            toReturn="Re-randomising list..."
        else:
            toReturn=self.answers.pop()
            inputs=":%s PRIVMSG %s :!%s"%(complete.userMask(), complete.channel(), toReturn)
            input=formatInput(pluginArguments(inputs))
            pluginOut=globalv.loadedPlugins[toReturn.split()[0]].action(input)
            return pluginOut

        return ["PRIVMSG $C$ :"+toReturn]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
