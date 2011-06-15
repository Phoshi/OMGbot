# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import re
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=str(complete.message()).strip()
        ttime=time.gmtime()
        result=""
        year=time.gmtime()[0]
        day=time.gmtime()[7]
        ignoreControlCharacters=True
        controlCharacters=['\x02', '\x1F', '\x16', '\x0F', '\x03']
        for letter in msg:
            if letter in controlCharacters:
                ignoreControlCharacters=False
        while not result:
            if not os.path.exists(os.path.join("logs","LogFile - "+complete.channel()+"-"+str(year) + "-" + str(day))):
                return ["PRIVMSG $C$ :No matches!"]
            with open(os.path.join("logs","LogFile - "+complete.channel()+"-"+str(year) + "-" + str(day))) as file:
                text=file.read()
            text=text.split('\n')
            for line in text:
                oline=line
                if ignoreControlCharacters:
                    line=re.sub("\x03\d*(,\d*)?","",line)
                    line=line.translate(None,''.join(controlCharacters))
                line=line.split('*')
                if len(line)!=1:
                    if len(line)==2:
                        line=' '.join(line[1].split()[1:])
                    else:
                        line=line[2]
                    if line.lower().find(msg.lower())!=-1:
                        if line.strip().startswith(globalv.commandCharacter)==False:
                            result=oline
            day-=1
            if day==0:
                year-=1
                day=365

        return ["PRIVMSG $C$ :"+result]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !last module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!last [phrase]"]
