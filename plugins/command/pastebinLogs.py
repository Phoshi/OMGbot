# -*- coding: utf-8 -*-
from plugins import plugin
import globalv, urllib2,urllib
import time
import datetime
import os
import re
import sys
sys.path.append("/home/py/.python/")
import datetime, dateutil.parser
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        arguments=complete.message().split()
        channel=complete.channel()
        msg=0
        perm=0
        timeFrom="00:00"
        hideUrls = False
        userPrint=[]
        print arguments

        for argument in arguments:
            print argument
            attemptedDate=False
            try:
                attemptedDate=dateutil.parser.parse(argument, dayfirst=True)
            except:
                pass #Awful practice, I know, but if dateparser fails it's probably because it wasn't given a date
            if argument.isdigit()==True and argument.find(':')==-1:
                msg=argument
                print "Got offset"
            elif attemptedDate!=False and argument.find(':')==-1:
                delta=(datetime.datetime.today()-attemptedDate)
                msg=delta.days
                print "Worked out offset", msg
            elif argument[0]=='#':
                channel=argument
                print "Figured channel"
            elif argument=="permanent":
                perm=1
                print "Set permenent"
            elif re.findall("[0-9]?[0-9]:[0-9][0-9]",argument)!=[]:
                timeFrom=re.findall("[0-9][0-9]:[0-9][0-9]",argument)[0]
                print "Got time"
            elif argument.lower()=="hideurls":
                hideUrls = True
            else:
                userPrint.append(argument)
                print "Got User"
        now=time.gmtime()
        year=now[0]
        day=now[7]-int(msg)
        while day<=0:
            year-=1
            day+=365
        output=[]
        cday=(datetime.date.today() - datetime.timedelta(int(msg))).day
        cmonth=(datetime.date.today() - datetime.timedelta(int(msg))).month
        fromTime=datetime.datetime(year,cmonth, cday, int(timeFrom.split(':')[0]), int(timeFrom.split(':')[1]))
        path=os.path.join("logs","LogFile - "+channel.lower()+"-"+str(year)+"-"+str(day))
        if not os.path.exists(path):
            return ["PRIVMSG $C$ :I have no logs for that day!"]
        with open(path) as file:
            for line in file.readlines():
                ctime=re.findall("[0-9][0-9]:[0-9][0-9]",line)
                if ctime!=[]:
                    ctime=ctime[0]
                    dtime=datetime.datetime(year,cmonth, cday, int(ctime.split(':')[0]), int(ctime.split(':')[1]))
                    try:
                        lineUser=line.split('*')[1].strip()
                    except Exception as detail:
                        lineUser=""
                    if dtime>=fromTime and (lineUser in userPrint or userPrint==[]):
                        if hideUrls:
                            line = line.replace('www.', 'www .').replace('http://', 'http ://').replace('https://', 'https ://')
                        output.append(line.strip())
        readFile='\n'.join(output)
        readFile="Log of %s on %s\n"%(channel,"%s-%s-%s"%(cday, cmonth, year))+readFile
        data={"paste_code":readFile,"paste_private":1,"paste_expire_date":"1H"}
        if perm:
            data["paste_expire_date"]="N"
        data=urllib.urlencode(data)
        req = urllib2.Request("http://pastebin.com/api_public.php", data)
        response = urllib2.urlopen(req)
        msg=response.read()
        print msg
        return ["PRIVMSG $C$ :"+msg+(" (Permanently)" if perm else " (Expires in 10 minutes)")+(" (URLs obfuscated to avoid spamfilter)" if hideUrls else "")]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !pastebinLogs module. I return a pastebin URL with the logs of today - [msg].","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!pastebinLogs [offset]"]
