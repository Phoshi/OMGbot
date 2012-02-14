# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import datetime
import time

datesToCountDownTo = ["2012/01/07 15:00", "2012/01/14 15:00", "2012/01/21 15:00", "2012/01/28 15:00", "2012/2/04 15:00"]

times = [("week", 7 * 24 * 60 * 60), ("day", 24 * 60 * 60), ("hour", 60*60), ("minute", 60)]
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def timeDiff(self, datestring):
        newDate = datetime.datetime.strptime(datestring, "%Y/%m/%d %H:%M")
        dateSeconds = time.mktime(newDate.timetuple())

        nowSeconds = time.time()

        difference = dateSeconds - nowSeconds
        return difference

    def timeTill(self, datestring):
        difference = self.timeDiff(datestring)
        timeDif = [0, 0, 0, 0]
        retString = []

        for timeIndex, timeEntry in enumerate(times):
            while difference > timeEntry[1]:
                difference-=timeEntry[1]
                timeDif[timeIndex]+=1
            if (timeDif[timeIndex] > 0):
                retString.append("%s %s%s"%(str(timeDif[timeIndex]), timeEntry[0], ("s" if timeDif[timeIndex]!=1 else "")))


        if (difference > 0):
            retString.append("%s %s%s"%(str(int(difference)), "second", ("s" if difference!=1 else "")))

        retString = ", ".join(retString[:-1]) + " and " + retString[-1]
        return retString

    def action(self, complete):
        if len(complete.message())==0:
            for hardcoded in datesToCountDownTo:
                if self.timeDiff(hardcoded) > 0:
                    return ["PRIVMSG $C$ :Next episode in "+self.timeTill(hardcoded)]
        return ["PRIVMSG $C$ :"+self.timeTill(complete.message())]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
