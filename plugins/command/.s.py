# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import shlex
import re
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=str(complete.message())
        print len(msg)
        print msg
        sender=complete.channel()
        try:
            ttime=time.gmtime()
            f = open(os.path.join("logs","LogFile - "+sender+"-"+str(ttime[0]) + "-" + str(ttime[7])))
            foundString="No results"
            lines = f.readlines()
            f.close()
            lines.reverse()
            try:
                terms=shlex.split(msg)[0]
                toReplace=' '.join(shlex.split(msg)[1:])
            except:
                terms=msg.split()[0]
                toReplace=' '.join(msg.split()[1:])
            for line in lines:
                mo = re.search('(^\[..? ... .. .?....] [*] [^\s]+ [*] .*'+terms+'.*)', line, re.I | re.DOTALL)
                if mo:
                    if mo.group(1).find(msg.rstrip())==-1 and mo.group(1).find('# The Topic is')==-1 and '*'.join(mo.group(1).split('*')[2:]).strip().startswith(globalv.commandCharacter)==False and mo.group(1).find('* '+globalv.miscVars[1]+' *')==-1:
                        foundString=mo.group(1)
                        break
            mo = re.search('^\[(.. ... ..) .....].+', foundString)
            match = ' '.join(foundString.split(' ')[5:])
            realMatch=match.split('*')
            if match.count('*')>0:
                toMessage=re.compile(terms, re.I|re.S).sub(toReplace, '*'.join(realMatch[1:]), 99)
                return ["PRIVMSG $C$ :"+"<"+realMatch[0].rstrip()+">"+toMessage[:600]]
            else:
                toMessage=re.compile(terms, re.I|re.S).sub(toReplace, '*'.join(realMatch[0:]), 99)
                toMessage.replace('ACTION','said')
                return ["PRIVMSG $C$ :"+toMessage]
        except Exception as detail:
            return ["PRIVMSG $C$ :Find and replace failure: "+str(detail)]

        return [""]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the ! module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!"]
