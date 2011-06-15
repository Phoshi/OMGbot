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
        toFind=shlex.split(complete.message())[0]
        toReplace=' '.join(shlex.split(complete.message())[1:])
        for line in lines:
            if re.findall(toFind, line)!=[] and re.findall("^\[.*?\] * .*? * !",line)==[]:
                line = line.split('*',1)[1] #To cut off the datetime string
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
                line = re.sub(toFind, toReplace, line) 
                if isAction:
                    line="* %s %s"%(user,line)
                else:
                    line="<%s> %s"%(user, line)
                return ["PRIVMSG $C$ :%s"%line]

        return ["PRIVMSG $C$ :Could not find %s in today's logs!"%toFind]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
