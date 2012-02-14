# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
from datetime import date
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init_db_tables__(self, name):
        if settingsHandler.tableExists("'"+name+"'")==False:
            settingsHandler.newTable("'"+name+"'","answer")
    def __init_answers__(self, complete):
        self.answers=[x[0] for x in settingsHandler.readSetting("'"+complete.cmd()[0]+"'","answer")]
    def __level__(self):
        return 0
    def __init__(self):
        self.answers=[]
    def action(self, complete):
        msg=complete.message()
        isElevated=(isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]))
        self.__init_answers__(complete)
        hashDate = True
        hashUser = True
        if len(msg.split())>=1:
            cmd=msg.split()[0]
            msg=' '.join(msg.split()[1:])
            if "-date" in msg.split():
                hashUser = False
            if "-user" in msg.split():
                hashDate = False
        else:
            cmd=""
            msg=""
        if cmd=="-add" and isElevated:
            settingsHandler.writeSetting("'"+complete.cmd()[0]+"'","answer",msg)
            toReturn="Added that answer"
            self.__init_answers__(complete)
        elif cmd=="-delete" and isElevated:
            settingsHandler.deleteSetting("'"+complete.cmd()[0]+"'","answer",msg)
            toReturn="Wiped that answer."
            self.__init_answers__(complete)
        elif cmd=="-wipe" and isElevated:
            settingsHandler.dropTable("'"+complete.cmd()[0]+"'")
            settingsHandler.newTable("'"+complete.cmd()[0]+"'","answer")
            toReturn="Answer table wiped!"
            self.__init_answers__(complete)
        elif cmd=="-dump":
            self.__init_answers__(complete)
            return ["PRIVMSG $C$ :[%s]"%', '.join(["'"+x+"'" for x in self.answers])]
        else:
            totalHash = 0
            if hashDate:
                totalHash += hash(date.today())
            if hashUser:
                totalHash += hash(complete.user())
            answer = totalHash % len(self.answers)
            print answer, totalHash, self.answers
            toReturn=self.answers[answer]
            if complete.message()=="":
                toReturn=toReturn.replace("$1$","$U$")
            else:
                toReturn=toReturn.replace("$1$",complete.message())
        return ["PRIVMSG $C$ :"+toReturn]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
