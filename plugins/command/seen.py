# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import os
import fnmatch

class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message().strip()
        sender=complete.channel()
        ttime=time.gmtime()
        result=""
        year=time.gmtime()[0]
        day=time.gmtime()[7]
        while not result:
            if not os.path.exists(os.path.join("logs","LogFile - "+sender+"-"+str(year) + "-" + str(day))):
                return ["PRIVMSG $C$ :No matches!"]
            with open(os.path.join("logs","LogFile - "+sender+"-"+str(year) + "-" + str(day))) as file:
                text=file.read()
            text=text.split('\n')
            text.reverse()
            for line in text:
                try:
                    oline=line
                    line=line.split('*')
                    if len(line)==1:
                        line=line[0]
                        if line.find('>')!=-1:
                            line=line.split('>')[1].split()[0]
                        if line.find('<')!=-1:
                            line=line.split('<')[1].split()[0]
                    if len(line)==2:
                        line=line[1].split()[0].strip()
                    else:
                        line=line[1].strip()
                    if fnmatch.fnmatch(line.lower(), msg.lower()):
                        print line
                        msgTime=oline.split(']')[0]+"]"
                        nowTime=time.strftime("[%d %b %y %H:%M]")
                        if msgTime!=nowTime:
                            result=oline
                            return ["PRIVMSG $C$ :"+result]
                except:
                    print line,"went badly (Module: seen)"
            day-=1
            if day==0:
                year-=1
                day=365
            print year, day
        return ["PRIVMSG $C$ :"+result]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !seen module. I find out when the last time a user was seen was.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!seen [user]"]
