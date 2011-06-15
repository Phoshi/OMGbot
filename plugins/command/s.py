# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import os
import shlex
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        ttime=time.gmtime()
        file = open(os.path.join("logs","LogFile - "+complete.channel()+"-"+str(ttime[0]) + "-" + str(ttime[7])))
        lines=file.readlines()
        lines.reverse()
        try:
            toFind=re.compile(shlex.split(complete.message())[0], re.I)
            toReplace=' '.join(shlex.split(complete.message())[1:])
        except Exception as detail:
            return ["PRIVMSG $C$ :%s"%detail]
        print "s starting: Matching %s and replacing with %s"%(toFind.pattern, toReplace)
        for line in lines:
            try:
                line = line.split('*',1)[1] #To cut off the datetime string
            except:
                print line
            if line.split()[1]=="*":
                newLine=line.split('*',1)[1]
            else:
                newLine=line.split(" ",1)[1]
            if toFind.search(newLine) and re.search("^ .*? \* "+globalv.commandCharacter,line) is None:
                if line.split()[1]=="*":
                    isAction=False
                else:
                    isAction=True
                if isAction:
                    user=line.split()[0]
                    line=line[len(user)+2:]
                else:
                    user=line.split()[0]
                    line=line[len(user+" * ")+1:]
                line = toFind.sub(toReplace, line) 
                if isAction:
                    line="* %s %s"%(user,line)
                else:
                    line="<%s> %s"%(user, line)
                return ["PRIVMSG $C$ :%s"%line[:600]]

        return ["PRIVMSG $C$ :Could not find %s in today's logs!"%toFind.pattern]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
