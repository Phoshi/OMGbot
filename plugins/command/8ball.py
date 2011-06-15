# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init_db_tables__(self, name):
        if settingsHandler.tableExists("'"+name+"'")==False:
            settingsHandler.newTable("'"+name+"'","answer")
            answers=["As I see it, yes","It is certain","It is decidedly so","Most likely","Outlook good","Signs point to yes", "Without a doubt", "Yes", "Yes - definitely","You may rely on it", "Reply hazy, try again","Ask again later", "Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful"]
            for answer in answers:
                settingsHandler.writeSetting("'"+name+"'", "answer",answer)
    def __init_answers__(self, complete):
        self.answers=[x[0] for x in settingsHandler.readSetting("'"+complete.cmd()[0]+"'","answer")]
        random.shuffle(self.answers)
    def __level__(self):
        return 0
    def __init__(self):
        self.answers=[]
    def action(self, complete):
        msg=complete.message()
        isElevated=(isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]))
        self.__init_answers__(complete)
        if len(msg.split())>=1:
            cmd=msg.split()[0]
            msg=' '.join(msg.split()[1:])
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
            toReturn=self.answers.pop()
            if complete.message()=="":
                toReturn=toReturn.replace("$1$","$U$")
            else:
                toReturn=toReturn.replace("$1$",complete.message())
        return ["PRIVMSG $C$ :"+toReturn]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
