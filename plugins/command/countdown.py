# -*- coding: utf-8 -*-
from plugins import plugin
from datetime import datetime
import globalv
import pickle
import os
import difflib

def daysTill(date):
    now=datetime.now()
    now = now.replace(hour=10)
    date = date.replace(hour=11)
    
    if date.year == 1900:
        if date.month > now.month:
            date=date.replace(year=now.year)
        elif date.month < now.month:
            date=date.replace(year=now.year+1)
        else:
            if date.day > now.day:
                date=date.replace(year=now.year)
            elif date.day < now.day:
                date=date.replace(year=now.year+1)
            else:
                return 0
    return (date-now).days

def parseDate(date):
    aa = monthName(date.month)+" "+str(date.day)
    if date.day%10==1 and date.day!=11:
        aa+="st"
    elif date.day%10==2 and date.day!=12:
        aa+="nd"
    elif date.day%10==3 and date.day!=13:
        aa+="rd"
    else:
        aa+="th"
    if date.year!=1900:
        aa+=" "+str(date.year)
    return aa

def monthName(month):
    return ["","January","February","March","April","May","June","July","August","September","October","November","December",][month]

def getDateFromString(eventdate,formats):
    eventdate=eventdate.replace("gust","____")
    eventdate=eventdate.replace("st","").replace("nd","").replace("rd","").replace("th","").replace("____","gust")
            
    validDate=False
    for dformat in formats:
        try:
            newdate = datetime.strptime(eventdate, dformat)
            validDate=True
            break
        except:
            validDate=False
    if not validDate:
        return False
    return newdate

def compareEvent(e1, e2):
    return daysTill(e1[1])-daysTill(e2[1])

class pluginClass(plugin):
    def __init__(self):
        self.events = []
        self.formats = [
            "%Y-%m-%d",    #2017-03-31
            "%B %d, %Y",   #March 31, 2017
            "%B %d %Y",    #March 31 2017
            "%d %B %Y",    #31 March 2017
            "%d %B",       #31 March
            "%B %d"       #March 31
            ]
    def gettype(self):
        return "command"
    
    def till(self,date):
        eventname=date
        
        eventExists = False
        for x in self.events:
            if x[0]==eventname:
                dd = daysTill(x[1])
                eventExists = True
                break

        if not eventExists:
            newdate=getDateFromString(eventname,self.formats)
            if newdate:
                eventExists = True
                dd=daysTill(newdate)

        if not eventExists:
            response = ["PRIVMSG $C$ :"+eventname+" has not been set as an event yet."]
            close_matches = difflib.get_close_matches(eventname, [x[0] for x in self.events])
            if len(close_matches) > 0:
                response.append("PRIVMSG $C$ :Did you mean: " + ', '.join(close_matches))
            return response
            
        if dd==0:
            return ["PRIVMSG $C$ :Today it's "+eventname+"!"]
        elif dd<0:
            return ["PRIVMSG $C$ :"+eventname+" happened "+str(-dd)+" days ago."]
        else:
            return ["PRIVMSG $C$ :"+str(dd)+" days till "+eventname]
        
    def action(self, complete):
        fileName="events-%s"%complete.cmd()[0]
        filePath=os.path.join("config",fileName)
        if os.path.exists(filePath):
            with open(filePath) as eventFile:
                self.events=pickle.load(eventFile)
        s=complete.message().split()
        if len(s)<1:
            return ["PRIVMSG $C$ :Invalid parameters"]
        if s[0]=="upcoming":
            upcoming = sorted([x for x in self.events if daysTill(x[1])>0],compareEvent)
            aa = "Upcoming: "
            for event in upcoming[:5]:
                aa += event[0] + " at " + parseDate(event[1]) + "; "
                
            return ["PRIVMSG $C$ :"+aa]
        if s[0]=="till":
            return self.till(' '.join(s[1:]))
        if s[0]=="set" or s[0]=="override":
            if not "as" in s:
                return ["PRIVMSG $C$ :Invalid usage; use: !countdown " + s[0] + " [Event name] as [Date]"]
            asPos=s.index("as")
            eventname=' '.join(s[1:asPos])
            ddate=' '.join(s[asPos+1:])

            eventFound = False
            
            for x in self.events:
                if x[0]==eventname:
                    if s[0]=="set":
                        return ["PRIVMSG $C$ :That event has already been set at " + parseDate(x[1]) + ". Use <!countdown override " + eventname + " as " + ddate + "> to override"]
                    else:
                        eventFound = True

            if not eventFound and s[0]=="override":
                response = ["PRIVMSG $C$ :"+eventname+" has not been set as an event yet."]
                close_matches = difflib.get_close_matches(eventname, [x[0] for x in self.events])
                if len(close_matches) > 0:
                    response.append("PRIVMSG $C$ :Did you mean: " + ', '.join(close_matches))
                return response

            newdate=getDateFromString(ddate,self.formats)
                    
            if newdate:
                if s[0]=="set":
                    self.events.append([eventname,newdate])
                else:
                    for x in range(len(self.events)):
                        if self.events[x][0]==eventname:
                            self.events[x][1]=newdate
                            
                with open(filePath,"w") as eventFile:
                    pickle.dump(self.events,eventFile)
                return ["PRIVMSG $C$ :"+eventname+" successfully added!"]
            else:
                return ["PRIVMSG $C$ :Invalid date format."]
        else:
            return self.till(' '.join(s[0:]))

        return ["PRIVMSG $C$ :Invalid Parameters"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !countdown module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!countdown set [Event name] as [Date]","PRIVMSG $C$ :!countdown (till) [Event name]"]
